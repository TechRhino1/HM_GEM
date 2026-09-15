"""
JARVIS AI 3.0 — Macroeconomic Event & Directional Shock Analyst Agent.
Features:
- Live Macro News Shock Directional Prediction (USD Bullish/Bearish impact on Gold, FX, Crypto)
- High-Impact Economic Event Blackout Window Management
- Session-Aware Macro Liquidity Bias
"""
import time
from typing import Dict, Any, List, Optional
from jarvis.data.schemas import MarketContext, RegimeOutput, AnalystReport, AnalystRole
from jarvis.analysts.base_analyst import BaseAnalyst


def _parse_metric(value: str) -> Optional[float]:
    """Parse a numeric macro metric, honouring %/K/M/B magnitude suffixes."""
    s = str(value).strip().replace("%", "")
    if not s:
        return None
    mult = 1.0
    if s[-1] in ("K", "k"):
        mult = 1_000.0
        s = s[:-1]
    elif s[-1] in ("M", "m"):
        mult = 1_000_000.0
        s = s[:-1]
    elif s[-1] in ("B", "b"):
        mult = 1_000_000_000.0
        s = s[:-1]
    try:
        return float(s) * mult
    except Exception:
        return None


class MacroAnalyst(BaseAnalyst):
    def __init__(self, news_calendar: Optional[List[Dict[str, Any]]] = None):
        super().__init__(AnalystRole.MACRO)
        self.news_calendar = news_calendar or []

    def analyze(self, context: MarketContext, regime: RegimeOutput) -> AnalystReport:
        t0 = time.perf_counter()
        evidence = []
        risk_factors = []

        score = 65.0
        bias = "NEUTRAL"
        sym = context.symbol.upper()

        # 1. Trading Session Liquidity Assessment
        session = context.session
        if session.is_prime_session:
            score += 15.0
            evidence.append(f"Institutional Prime Session Active ({session.current_session}).")
        else:
            evidence.append(f"Off-hours / Asian liquidity session ({session.current_session}).")
            if session.current_session == "ASIAN":
                risk_factors.append("Asian session low volume; high risk of false breakouts.")
                score -= 10.0

        # 2. Real-Time Macro News Directional Shock Scoring
        if not self.news_calendar:
            try:
                from jarvis.market.news import GLOBAL_NEWS_ENGINE
                active_news = GLOBAL_NEWS_ENGINE.get_news_calendar()
            except Exception:
                active_news = []
        else:
            active_news = self.news_calendar

        usd_bull_shock = False
        usd_bear_shock = False
        active_shock_event = None

        for item in active_news:
            curr = item.get("currency", "")
            impact = item.get("impact", "")
            actual_str = str(item.get("actual", ""))
            fcst_str = str(item.get("forecast", ""))
            event_name = str(item.get("event", "")).lower()
            diff_sec = item.get("diff_seconds")

            if curr == "USD" and impact == "HIGH":
                # Upcoming event in next 15 minutes: volatility blackout / buffer warning
                if diff_sec is not None and 0 < diff_sec <= 900:
                    risk_factors.append(f"⏳ Upcoming HIGH-impact USD event: {item.get('event')} in {int(diff_sec/60)}m — volatility spike imminent.")
                    score -= 5.0
                    continue

                # Skip events that haven't released yet or are > 15m in the future
                if not actual_str or actual_str in ("Upcoming", "—", "", "Pending") or (diff_sec is not None and diff_sec > 900):
                    continue

                # SHOCK FRESHNESS WINDOW: Only active within 45 minutes of release (-2700s <= diff_sec <= 0)
                # Releases older than 45 minutes are fully digested / priced in by the interbank market
                if diff_sec is not None and diff_sec < -2700:
                    continue

                try:
                    act = _parse_metric(actual_str)
                    fcst = _parse_metric(fcst_str)
                    if act is None or fcst is None:
                        continue

                    diff_val = act - fcst
                    if abs(diff_val) < 1e-5:
                        continue  # In line with forecast — neutral outcome

                    # Detect inverse indicators where higher actual = weaker USD
                    is_inverse = any(kw in event_name for kw in [
                        "jobless", "unemployment", "trade deficit", "deficit"
                    ])

                    if is_inverse:
                        if act > fcst:
                            usd_bear_shock = True
                            active_shock_event = item.get("event")
                            evidence.append(f"Active Macro Shock (Weaker USD): {item.get('event')} {actual_str} vs {fcst_str} fcst (Released {abs(int((diff_sec or 0)/60))}m ago).")
                        elif act < fcst:
                            usd_bull_shock = True
                            active_shock_event = item.get("event")
                            evidence.append(f"Active Macro Shock (Stronger USD): {item.get('event')} {actual_str} vs {fcst_str} fcst (Released {abs(int((diff_sec or 0)/60))}m ago).")
                    else:
                        if act > fcst:
                            usd_bull_shock = True
                            active_shock_event = item.get("event")
                            evidence.append(f"Active Macro Shock (Stronger USD): {item.get('event')} {actual_str} vs {fcst_str} fcst (Released {abs(int((diff_sec or 0)/60))}m ago).")
                        elif act < fcst:
                            usd_bear_shock = True
                            active_shock_event = item.get("event")
                            evidence.append(f"Active Macro Shock (Weaker USD): {item.get('event')} {actual_str} vs {fcst_str} fcst (Released {abs(int((diff_sec or 0)/60))}m ago).")
                except Exception:
                    continue

        # 3. Canonical Cross-Asset Directional Bias Mapping
        try:
            from jarvis.data.symbol_registry import resolve as resolve_sym
            spec = resolve_sym(sym)
            canonical = spec.canonical.upper() if spec else sym
        except Exception:
            canonical = sym

        # USD-Inversed Assets: Gold, Major Currencies, Cryptos
        usd_inverse_assets = {"XAUUSD", "EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "BTCUSD", "ETHUSD", "SOLUSD"}
        # USD-Correlated Assets: USDJPY, USDCAD, USDCHF
        usd_correlated_assets = {"USDJPY", "USDCAD", "USDCHF"}
        # Equity Indices: Sensitive to Rate Shocks
        equity_index_assets = {"US500", "NAS100", "US30", "GER40", "UK100"}

        if canonical in usd_inverse_assets or any(k in sym for k in ["XAU", "GOLD", "EUR", "GBP", "AUD", "NZD", "BTC", "ETH", "SOL"]):
            if usd_bull_shock:
                bias = "BEARISH"
                score += 15.0
                evidence.append(f"Macro Directional Catalyst: Strong USD shock ({active_shock_event}) creates institutional headwind on {sym}.")
            elif usd_bear_shock:
                bias = "BULLISH"
                score += 15.0
                evidence.append(f"Macro Directional Catalyst: Weak USD shock ({active_shock_event}) triggers institutional BUY impulse on {sym}.")

        elif canonical in usd_correlated_assets or any(k in sym for k in ["USDJPY", "USDCAD", "USDCHF"]):
            if usd_bull_shock:
                bias = "BULLISH"
                score += 15.0
                evidence.append(f"Macro Directional Catalyst: Strong USD yield rally ({active_shock_event}) drives institutional BUY bias on {sym}.")
            elif usd_bear_shock:
                bias = "BEARISH"
                score += 15.0
                evidence.append(f"Macro Directional Catalyst: Weak USD yields ({active_shock_event}) trigger institutional SELL flow on {sym}.")

        elif canonical in equity_index_assets or any(k in sym for k in ["US500", "NAS100", "US30", "SPX", "NDX", "DJI", "GER40", "UK100"]):
            if usd_bull_shock:
                bias = "BEARISH"
                score += 15.0
                evidence.append(f"Macro Directional Catalyst: Hawkish yield shock ({active_shock_event}) pressures equity valuations on {sym}.")
            elif usd_bear_shock:
                bias = "BULLISH"
                score += 15.0
                evidence.append(f"Macro Directional Catalyst: Dovish monetary relief ({active_shock_event}) fuels equity risk-on impulse on {sym}.")

        elif "WTI" in canonical or any(k in sym for k in ["OIL", "CRUDE", "WTI"]):
            if usd_bull_shock:
                bias = "BEARISH"
                score += 10.0
                evidence.append(f"Macro: Dollar strength pressures USD-denominated energy commodities ({sym}).")
            elif usd_bear_shock:
                bias = "BULLISH"
                score += 10.0
                evidence.append(f"Macro: Dollar softening supports energy commodity pricing ({sym}).")

        # 3b. Fallback: No active macro shock — align with structural order flow
        # "No news is good news" — absence of macro headwinds supports prevailing trend structure.
        if bias == "NEUTRAL" and not usd_bull_shock and not usd_bear_shock:
            structure_bias = context.structure.bias
            if structure_bias in ("BULLISH", "BEARISH"):
                bias = structure_bias
                evidence.append(f"Macro: No active high-impact macro shock active — aligning with {structure_bias} market structure.")

        # 4. Check regime event risk / blackout window
        if regime.primary_regime.value == "EVENT_RISK":
            score = 30.0
            risk_factors.append("High-impact economic event active — wide spreads and slippage expected.")

        final_score = min(100.0, max(0.0, score))
        confidence = min(0.95, max(0.40, final_score / 100.0))
        elapsed = (time.perf_counter() - t0) * 1000.0

        return AnalystReport(
            role=self.role,
            symbol=context.symbol,
            bias=bias,
            score=round(final_score, 1),
            confidence=round(confidence, 2),
            evidence=evidence,
            risk_factors=risk_factors,
            execution_time_ms=round(elapsed, 2),
            metadata={"session": session.current_session, "is_prime": session.is_prime_session, "usd_bull_shock": usd_bull_shock}
        )
