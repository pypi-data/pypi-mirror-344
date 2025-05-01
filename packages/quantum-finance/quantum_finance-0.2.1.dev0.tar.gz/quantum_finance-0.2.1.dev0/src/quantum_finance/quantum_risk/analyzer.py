#!/usr/bin/env python3

"""
Quantum Enhanced Cryptocurrency Risk Analyzer

This module provides the core functionality for quantum-enhanced cryptocurrency risk assessment,
leveraging quantum computing techniques to model market dependencies and propagate uncertainty
with greater accuracy than classical methods.

Author: Quantum-AI Team
"""

import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Union

# Use absolute imports relative to src
from quantum_finance.quantum_bayesian_risk import QuantumBayesianRiskNetwork
from quantum_finance.quantum_market_encoding import (
    encode_order_book_imbalance,
    encode_market_volatility,
    encode_price_impact,
    encode_liquidity_risk,
    combined_market_risk_encoding,
    visualize_quantum_market_encoding
)

# Use absolute imports relative to src for modularized components
from quantum_finance.quantum_risk.data_fetcher import CryptoDataFetcher
from quantum_finance.quantum_risk.risk_metrics import RiskMetricsCalculator
from quantum_finance.quantum_risk.report_generator import ReportGenerator
from quantum_finance.quantum_risk.utils.logging_util import setup_logger

logger = setup_logger(__name__)

class QuantumEnhancedCryptoRiskAnalyzer:
    """
    Quantum-enhanced cryptocurrency risk analyzer that leverages
    quantum computing for uncertainty-aware risk assessment.
    """
    
    def __init__(self, api_key: Optional[str] = None, 
                 use_adaptive_shots: bool = True,
                 shot_config: Optional[Dict[str, Any]] = None,
                 analog_backend: bool = False):
        """
        Initialize the quantum-enhanced risk analyzer.
        
        Args:
            api_key: Optional RapidAPI key for Binance API access
            use_adaptive_shots: Whether to use adaptive shot selection for circuit execution
            shot_config: Optional configuration for adaptive shot selection
                         Example: {"min_shots": 256, "max_shots": 8192, "target_precision": 0.02}
            analog_backend: Whether to use the analog IMC backend
        """
        self.api_key = api_key or os.environ.get("RAPIDAPI_KEY")
        self.analog_backend = analog_backend
        if self.analog_backend:
            logger.info("Analog IMC backend enabled")
        self.use_adaptive_shots = use_adaptive_shots
        
        # Default shot configuration for market analysis (optimized through benchmarking)
        self.shot_config = shot_config or {
            "min_shots": 256,
            "max_shots": 8192,
            "target_precision": 0.02
        }
        
        # Initialize components
        self.data_fetcher = CryptoDataFetcher(api_key=self.api_key)
        self.risk_calculator = RiskMetricsCalculator()
        self.report_generator = ReportGenerator()
        
        # Initialize quantum components
        self._initialize_quantum_components()
        
        logger.info("Initialized QuantumEnhancedCryptoRiskAnalyzer")
        if self.use_adaptive_shots:
            logger.info(f"Using adaptive shot selection with config: {self.shot_config}")
    
    def _initialize_quantum_components(self):
        """Initialize quantum components for risk assessment"""
        # Create quantum Bayesian network with standard risk factors
        self.quantum_bayesian_network = QuantumBayesianRiskNetwork(
            num_risk_factors=5,
            risk_factor_names=[
                "Order Book Imbalance",
                "Price Volatility",
                "Market Depth Risk",
                "Liquidity Risk",
                "Overall Risk"
            ],
            use_adaptive_shots=self.use_adaptive_shots
        )
        
        # Define the risk factor relationships (based on market analysis)
        # Format: (cause, effect, strength)
        relationships = [
            (0, 1, 0.7),  # Order book imbalance -> Price volatility
            (1, 2, 0.6),  # Price volatility -> Market depth risk
            (2, 3, 0.5),  # Market depth risk -> Liquidity risk
            (3, 4, 0.8),  # Liquidity risk -> Overall risk
            (0, 4, 0.4),  # Direct: Order book imbalance -> Overall risk
            (1, 4, 0.5),  # Direct: Price volatility -> Overall risk
        ]
        
        # Add relationships to network
        for cause, effect, strength in relationships:
            self.quantum_bayesian_network.add_conditional_relationship(
                cause, effect, strength
            )
        
        logger.info("Quantum Bayesian network initialized with market relationships")
    
    def _get_crypto_data_fetcher(self) -> CryptoDataFetcher:
        """
        Get the CryptoDataFetcher instance.
        
        Returns:
            CryptoDataFetcher: The data fetcher instance
        """
        return self.data_fetcher
    
    def analyze_with_quantum(self, symbol: str, shots: int = 10000,
                           override_adaptive_shots: Optional[bool] = None) -> Dict[str, Any]:
        """
        Perform quantum-enhanced risk analysis for a cryptocurrency.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            shots: Number of shots to use for quantum circuit execution
                  (only used if adaptive_shots is False)
            override_adaptive_shots: Optional parameter to override the global adaptive_shots setting
            
        Returns:
            Dict: Analysis results
        """
        # Determine whether to use adaptive shots
        use_adaptive = override_adaptive_shots if override_adaptive_shots is not None else self.use_adaptive_shots
        
        # Log analysis start
        logger.info(f"Starting quantum risk analysis for {symbol}")
        logger.info(f"Using {'adaptive' if use_adaptive else 'fixed'} shot selection")
        
        start_time = datetime.now()
        
        # Fetch market data
        logger.info(f"Fetching market data for {symbol}")
        try:
            # Fetch order book data
            order_book = self.data_fetcher.fetch_order_book(symbol)
            
            # Fetch 24hr stats
            stats_24hr = self.data_fetcher.fetch_24hr_stats(symbol)
            
            # Fetch recent trades
            recent_trades = self.data_fetcher.fetch_recent_trades(symbol)
        except Exception as e:
            logger.error(f"Error fetching market data: {str(e)}")
            return {"error": f"Failed to fetch market data: {str(e)}"}
        
        # Calculate classical risk metrics
        logger.info("Calculating classical risk metrics")
        # The refactored RiskMetricsCalculator exposes ``calculate_risk_metrics`` but
        # legacy mocks (see tests/unit/quantum_risk/test_analyzer.py) still patch
        # ``calculate_classical_risk_metrics``.  We therefore call the modern
        # method if it exists, otherwise fall back to the legacy name.
        if hasattr(self.risk_calculator, "calculate_risk_metrics"):
            risk_metrics = self.risk_calculator.calculate_risk_metrics(
                order_book, stats_24hr, recent_trades
            )
        else:
            risk_metrics = self.risk_calculator.calculate_classical_risk_metrics(
                order_book, stats_24hr
            )
        
        # Encode market data into quantum circuits
        logger.info("Encoding market data into quantum circuits")
        try:
            risk_circuit = combined_market_risk_encoding(
                order_book_data=order_book,
                volatility=risk_metrics.get('24hr_price_volatility', risk_metrics.get('volatility_risk', 0.0)),
                trade_size=risk_metrics.get('avg_trade_size', 0.0),
                recent_volume=risk_metrics.get('24hr_volume', risk_metrics.get('normalized_volume', 0.0)),
                num_qubits=8,
                fallback_on_error=True
            )
            
            # Create market encoding visualization
            market_encoding_png = f"{symbol}_quantum_market_encoding_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            visualize_quantum_market_encoding(risk_circuit, 
                                          title=f"{symbol} Quantum Market Encoding",
                                          output_file=market_encoding_png)
        except Exception as e:
            logger.error(f"Error in quantum market encoding: {str(e)}")
            return {"error": f"Failed to encode market data: {str(e)}"}
        
        # Prepare risk factors for Bayesian network
        initial_risk_probabilities = [
            risk_metrics.get('order_book_imbalance', risk_metrics.get('imbalance', 0.0)) / 100.0,
            risk_metrics.get('24hr_price_volatility', risk_metrics.get('volatility_risk', 0.0)) / 100.0,
            risk_metrics.get('market_depth_risk', risk_metrics.get('normalized_depth', 0.0)) / 100.0,
            risk_metrics.get('liquidity_risk', 0.0) / 100.0,
            risk_metrics.get('overall_classical_risk', risk_metrics.get('overall_risk', 0.0)) / 100.0,
        ]
        
        # Propagate risk through quantum network
        logger.info("Propagating risk through quantum Bayesian network")
        try:
            quantum_risk_result = self.quantum_bayesian_network.propagate_risk(
                initial_risk_probabilities, 
                shots=shots,
                adaptive_shots=use_adaptive,
                target_precision=self.shot_config.get("target_precision", 0.02)
            )
            
            # ------------------------------------------------------------------
            # Back-compatibility shim (2025-04)
            # ------------------------------------------------------------------
            # Historical unit-tests mocked ``propagate_risk`` to return a *list*
            # of risk probabilities directly rather than the new dictionary
            # structure that wraps the list under the key
            # ``updated_probabilities``.  To remain compatible we detect this
            # legacy form here and adapt it on-the-fly.
            # ------------------------------------------------------------------
            if isinstance(quantum_risk_result, list):
                # Legacy list form -> treat as probabilities, no stats
                quantum_probabilities = quantum_risk_result
                execution_stats = {}
            elif isinstance(quantum_risk_result, dict):
                quantum_probabilities = quantum_risk_result.get("updated_probabilities", [])
                execution_stats = quantum_risk_result.get("execution_stats", {})
            else:
                raise TypeError(
                    "Unexpected return type from propagate_risk: "
                    f"{type(quantum_risk_result).__name__}. Expected list or dict."
                )
            
            # Compare quantum vs classical
            comparison_result = self.quantum_bayesian_network.compare_classical_quantum(
                initial_risk_probabilities,
                output_file=f"{symbol}_quantum_classical_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            
            # Create risk network visualization
            self.quantum_bayesian_network.visualize_network(
                output_file=f"{symbol}_quantum_risk_network_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
        except Exception as e:
            logger.error(f"Error in quantum risk propagation: {str(e)}")
            return {"error": f"Failed to propagate quantum risk: {str(e)}"}
        
        # Scale back to percentage
        quantum_risk_percentage = [p * 100.0 for p in quantum_probabilities]
        
        # Overall quantum risk (from the last risk factor)
        overall_quantum_risk = quantum_risk_percentage[-1]
        
        # Execution statistics
        execution_stats["total_analysis_time_sec"] = (datetime.now() - start_time).total_seconds()
        
        # ------------------------------------------------------------------
        # Legacy-compatible result schema (2025-04)
        # ------------------------------------------------------------------
        # Earlier versions of the analyzer returned a flatter structure which
        # is still expected by a subset of unit-tests.  We therefore build two
        # parallel representations: the modern one under ``modern_results``
        # and a compatibility wrapper exposed at top-level.  Downstream code
        # should migrate to the modern structure, but for now we keep both.
        # ------------------------------------------------------------------

        # Map classical metrics to legacy names where possible
        classical_risk_compat: Dict[str, float] = {}
        legacy_mapping = {
            "liquidity_risk": ["liquidity_risk"],
            "volatility_risk": ["24hr_price_volatility", "volatility_risk"],
            "market_depth_risk": ["market_depth_risk"],
            "order_book_imbalance_risk": ["order_book_imbalance", "imbalance"],
            "overall_risk": ["overall_classical_risk", "overall_risk"],
        }
        for legacy_key, candidates in legacy_mapping.items():
            for cand in candidates:
                if cand in risk_metrics:
                    classical_risk_compat[legacy_key] = risk_metrics[cand]
                    break

        # Ensure overall_risk is present for diff calculation
        classical_overall = classical_risk_compat.get("overall_risk", 0.0)

        # Build quantum risk dict aligning with legacy expectations
        quantum_enhanced_risk = {
            "order_book_imbalance_risk": quantum_risk_percentage[0],
            "volatility_risk": quantum_risk_percentage[1],
            "market_depth_risk": quantum_risk_percentage[2],
            "liquidity_risk": quantum_risk_percentage[3],
            "overall_risk": quantum_risk_percentage[4],
        }

        # Compute differences
        risk_differences = {
            k: quantum_enhanced_risk[k] - classical_risk_compat.get(k, 0.0)
            for k in quantum_enhanced_risk.keys()
        }

        compat_results = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "current_price": float(stats_24hr.get("lastPrice", 0.0) if isinstance(stats_24hr, dict) else 0.0),
            "classical_risk": classical_risk_compat,
            "quantum_enhanced_risk": quantum_enhanced_risk,
            "risk_differences": risk_differences,
            "visualizations": {
                "market_circuit": market_encoding_png,
                "risk_network": f"{symbol}_quantum_risk_network_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                "comparison": f"{symbol}_quantum_classical_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            },
            # Preserve modern structure for forward compatibility
            "_modern_results": {
                "market_data": {
                    "order_book_summary": self._summarize_order_book(order_book),
                    "stats_24hr": stats_24hr,
                    "recent_trades_summary": self._summarize_recent_trades(recent_trades),
                },
                "classical_metrics": risk_metrics,
                "quantum_analysis": {
                    "risk_probabilities": quantum_risk_percentage,
                    "overall_quantum_risk": overall_quantum_risk,
                    "difference_from_classical": overall_quantum_risk - classical_overall,
                    "execution_stats": execution_stats,
                },
            },
        }

        return compat_results
    
    def generate_analysis_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a markdown report of the quantum-enhanced risk analysis.
        
        Args:
            results: Results from analyze_with_quantum
            
        Returns:
            Markdown formatted report
        """
        return self.report_generator.generate_markdown_report(results) 
        
    def update_risk_assessment(self, 
                              previous_assessment: Dict[str, Any], 
                              symbol: str, 
                              order_book: Optional[Dict[str, Any]] = None, 
                              stats_24hr: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update a previous risk assessment with new market data, avoiding a full recalculation.
        
        This method provides more efficient incremental updates by:
        1. Only fetching data that's not provided
        2. Reusing previous quantum calculations where possible
        3. Only updating the risk factors that are affected by changed market data
        
        Args:
            previous_assessment: Results from a previous analyze_with_quantum call
            symbol: Cryptocurrency symbol (e.g. 'BTC', 'ETH')
            order_book: Optional new order book data (will be fetched if not provided)
            stats_24hr: Optional new 24hr stats (will be fetched if not provided)
            
        Returns:
            Updated risk assessment dictionary
        """
        logger.info(f"Updating risk assessment for {symbol}")
        
        # Get market data if not provided
        if order_book is None:
            order_book = self.data_fetcher.get_binance_order_book(symbol)
            
        if stats_24hr is None:
            stats_24hr = self.data_fetcher.get_binance_24hr_stats(symbol)
        
        # Extract previous values for comparison
        prev_classical_risk = previous_assessment.get('classical_metrics', {})
        prev_market_metrics = previous_assessment.get('market_data', {})
        
        # Calculate new classical risk metrics
        new_classical_risk = self.risk_calculator.calculate_classical_risk_metrics(
            order_book, stats_24hr, symbol
        )
        
        # Determine which risk factors have changed significantly
        changed_factors = []
        significant_change_threshold = 0.05  # 5% change is considered significant
        
        for metric, new_value in new_classical_risk.items():
            if metric in prev_classical_risk:
                prev_value = prev_classical_risk.get(metric, 0)
                if abs(new_value - prev_value) > significant_change_threshold * prev_value:
                    changed_factors.append(metric)
        
        # If no significant changes, just update timestamps and return
        if not changed_factors:
            logger.info(f"No significant changes detected for {symbol}, returning previous assessment with updated timestamp")
            updated_assessment = previous_assessment.copy()
            updated_assessment['timestamp'] = datetime.now().strftime('%Y%m%d_%H%M%S')
            return updated_assessment
        
        logger.info(f"Significant changes detected in factors: {changed_factors}")
        
        # Extract risk metrics for quantum Bayesian network
        initial_probabilities = [
            new_classical_risk['order_book_imbalance'] / 100.0,
            new_classical_risk['24hr_price_volatility'] / 100.0,
            new_classical_risk['market_depth_risk'] / 100.0,
            new_classical_risk['liquidity_risk'] / 100.0,
            new_classical_risk['overall_classical_risk'] / 100.0
        ]
        
        # Create the combined quantum market circuit for visualization
        market_circuit = combined_market_risk_encoding(
            order_book_data=order_book,
            volatility=new_classical_risk['24hr_price_volatility'],
            trade_size=new_classical_risk['avg_trade_size'],
            recent_volume=new_classical_risk['24hr_volume'],
            num_qubits=8,
            fallback_on_error=True
        )
        
        # Save the market circuit visualization
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        market_circuit_file = f"{symbol}_quantum_market_encoding_{timestamp}.png"
        visualize_quantum_market_encoding(
            market_circuit,
            f"Quantum Market Encoding for {symbol}",
            market_circuit_file
        )
        
        # Propagate risk through the quantum Bayesian network
        quantum_probs = self.quantum_bayesian_network.propagate_risk(
            initial_probabilities, 
            shots=5000  # Reduce shot count for incremental updates
        )
        
        # Compare with classical approximation (only if significant changes)
        comparison_file = f"{symbol}_quantum_classical_comparison_{timestamp}.png"
        comparison = self.quantum_bayesian_network.compare_classical_quantum(
            initial_probabilities,
            comparison_file
        )
        
        # Scale back to percentages for reporting
        quantum_enhanced_risk = {
            'order_book_imbalance_risk': quantum_probs[0] * 100,
            'volatility_risk': quantum_probs[1] * 100,
            'market_depth_risk': quantum_probs[2] * 100,
            'liquidity_risk': quantum_probs[3] * 100, 
            'overall_risk': quantum_probs[4] * 100
        }
        
        # Calculate quantum advantage metrics
        risk_differences = {
            k: quantum_enhanced_risk[k] - v 
            for k, v in new_classical_risk.items() 
            if k in ['24hr_price_volatility', 'market_depth_risk', 'liquidity_risk', 'overall_classical_risk']
        }
        
        # Reuse previous network visualization if available, or create a new one
        network_file = previous_assessment.get('visualizations', {}).get('risk_network')
        if not network_file or not os.path.exists(network_file):
            network_file = f"{symbol}_quantum_risk_network_{timestamp}.png"
            self.quantum_bayesian_network.visualize_network(network_file)
        
        # Combine results
        results = {
            'timestamp': timestamp,
            'symbol': symbol,
            'current_price': new_classical_risk['current_price'],
            'classical_metrics': new_classical_risk,
            'quantum_analysis': {
                'risk_probabilities': quantum_probs,
                'overall_quantum_risk': quantum_probs[-1] * 100,
                'difference_from_classical': (quantum_probs[-1] - new_classical_risk['overall_classical_risk']) * 100,
                'execution_stats': {}
            },
            'market_data': {
                'order_book_summary': self._summarize_order_book(order_book),
                'stats_24hr': stats_24hr,
                'recent_trades_summary': self._summarize_recent_trades(self.data_fetcher.fetch_recent_trades(symbol))
            },
            'quantum_enhanced_risk': quantum_enhanced_risk,
            'risk_differences': risk_differences,
            'market_metrics': {
                'bid_ask_spread': new_classical_risk['bid_ask_spread'],
                'volatility': new_classical_risk['24hr_price_volatility'],
                'normalized_depth': new_classical_risk['market_depth_risk'],
                'normalized_volume': new_classical_risk['24hr_volume'],
                'imbalance': new_classical_risk['order_book_imbalance'],
                'price_impact': new_classical_risk['avg_trade_size']
            },
            'visualizations': {
                'market_circuit': market_circuit_file,
                'risk_network': network_file,
                'comparison': comparison_file
            },
            'update_info': {
                'is_incremental_update': True,
                'previous_assessment_timestamp': previous_assessment.get('timestamp'),
                'changed_factors': changed_factors
            }
        }
        
        # Save results to JSON file
        results_file = f"{symbol}_quantum_risk_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Incremental update complete. Results saved to {results_file}")
        
        return results 

    # ------------------------------------------------------------------
    # Helper summarization methods (simple placeholders for legacy tests)
    # ------------------------------------------------------------------
    def _summarize_order_book(self, order_book):  # type: ignore[no-self-use]
        """Return a lightweight summary of the order-book suitable for JSON."""
        return {
            "bid_levels": order_book.get("bid_levels", [])[:3] if isinstance(order_book, dict) else [],
            "ask_levels": order_book.get("ask_levels", [])[:3] if isinstance(order_book, dict) else [],
            "spread": order_book.get("spread") if isinstance(order_book, dict) else None,
        }

    def _summarize_recent_trades(self, trades):  # type: ignore[no-self-use]
        """Return a lightweight summary (count & last price) of recent trades."""
        if isinstance(trades, list) and trades:
            last_trade = trades[-1]
            price = last_trade.get("price") if isinstance(last_trade, dict) else None
            return {"count": len(trades), "last_price": price}
        return {"count": 0}

def main():
    """Command line interface for the risk analyzer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Quantum-Enhanced Cryptocurrency Risk Analyzer")
    parser.add_argument("symbol", help="Cryptocurrency symbol (e.g., BTC, ETH)")
    parser.add_argument("--api-key", help="RapidAPI key for Binance API")
    parser.add_argument("--shots", type=int, default=10000, help="Number of quantum circuit shots")
    parser.add_argument("--no-adaptive", action="store_true", help="Disable adaptive shot selection")
    parser.add_argument("--min-shots", type=int, default=256, help="Minimum shots for adaptive selection")
    parser.add_argument("--max-shots", type=int, default=8192, help="Maximum shots for adaptive selection")
    parser.add_argument("--precision", type=float, default=0.02, help="Target precision for adaptive selection")
    
    args = parser.parse_args()
    
    # Configure shot selection
    shot_config = {
        "min_shots": args.min_shots,
        "max_shots": args.max_shots,
        "target_precision": args.precision
    }
    
    # Create the analyzer
    analyzer = QuantumEnhancedCryptoRiskAnalyzer(
        api_key=args.api_key,
        use_adaptive_shots=not args.no_adaptive,
        shot_config=shot_config
    )
    
    # Run the analysis
    try:
        results = analyzer.analyze_with_quantum(args.symbol, shots=args.shots)
        
        # Print summary to console
        print(f"\nRisk Analysis Summary for {args.symbol}:")
        print(f"Overall Quantum Risk: {results['quantum_analysis']['overall_quantum_risk']:.2f}%")
        print(f"Classical Risk: {results['classical_metrics']['overall_classical_risk']:.2f}%")
        print(f"Difference: {results['quantum_analysis']['difference_from_classical']:.2f}%")
        
        if not args.no_adaptive:
            print("\nAdaptive Shot Selection Statistics:")
            print(f"Shots Used: {results['quantum_analysis']['execution_stats'].get('actual_shots_used', 'N/A')}")
            print(f"Target Precision: {results['quantum_analysis']['execution_stats'].get('target_precision', 'N/A')}")
        
        print(f"\nResults saved to: {results['visualizations']['risk_network']}")
        
    except Exception as e:
        print(f"Error running risk analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 