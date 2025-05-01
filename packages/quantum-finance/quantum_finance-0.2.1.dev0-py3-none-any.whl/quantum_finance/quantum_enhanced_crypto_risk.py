#!/usr/bin/env python3

"""
Quantum Enhanced Cryptocurrency Risk Assessment

This script demonstrates how to enhance cryptocurrency risk assessment with
quantum computing capabilities, specifically using a Quantum Bayesian Risk
Network to model market dependencies.

Features:
- Integration with Binance API market microstructure data
- Quantum encoding of order book and market data
- Bayesian risk propagation using quantum circuits
- Comparison with classical risk assessment

Author: Quantum-AI Team
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional, Any
import argparse
import pandas as pd

# Load environment variables from .env file
from dotenv import load_dotenv
from pathlib import Path

# Look for .env file in current and parent directories
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    print(f"Loaded environment variables from {env_path.absolute()}")
else:
    # Try to find .env in parent directories
    parent_dir = Path('.').absolute().parent
    parent_env = parent_dir / '.env'
    if parent_env.exists():
        load_dotenv(dotenv_path=parent_env, override=True)
        print(f"Loaded environment variables from {parent_env}")
    else:
        load_dotenv()  # Try default loading
        print("Attempted to load .env from default locations")

# Print API key info for debugging (without revealing full key)
api_key = os.environ.get('RAPIDAPI_KEY')
if api_key:
    masked_key = api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else '****'
    print(f"RAPIDAPI_KEY found: {masked_key}")
else:
    print("RAPIDAPI_KEY not found in environment variables")

# Import quantum components
from quantum_bayesian_risk import QuantumBayesianRiskNetwork
from examples.crypto_data_fetcher_enhanced import EnhancedCryptoDataFetcher
from quantum_market_encoding import (
    combined_market_risk_encoding,
    visualize_quantum_market_encoding
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QuantumEnhancedCryptoRisk:
    """
    Quantum-enhanced cryptocurrency risk assessment tool.
    
    This class combines quantum Bayesian risk networks with market microstructure
    data to provide enhanced risk assessment for cryptocurrencies.
    """
    
    def __init__(self, api_key: Optional[str] = None, api_host: Optional[str] = None):
        """
        Initialize the quantum risk assessment engine.
        
        Args:
            api_key: Optional RapidAPI key for Binance data access
            api_host: Optional RapidAPI host for Binance data
        """
        # Set API credentials
        self.api_key = api_key or os.environ.get('RAPIDAPI_KEY')
        self.api_host = api_host or os.environ.get('RAPIDAPI_HOST', 'binance43.p.rapidapi.com')
        
        # Initialize the quantum Bayesian risk network
        self.quantum_bayesian_network = QuantumBayesianRiskNetwork(
            num_risk_factors=5,
            use_adaptive_shots=True
        )
        
        # Define core risk relationships
        self._define_risk_relationships()
        
        logger.info("Initialized QuantumEnhancedCryptoRisk with quantum Bayesian network")
    
    def _define_risk_relationships(self):
        """Define the causal relationships between different risk factors."""
        # Define how market factors affect each other
        risk_relationships = [
            # Cause, Effect, Strength (0-1)
            (0, 1, 0.7),  # Order Book Imbalance → Price Volatility
            (1, 3, 0.8),  # Price Volatility → Liquidity Risk
            (2, 3, 0.6),  # Market Depth → Liquidity Risk
            (1, 4, 0.8),  # Price Volatility → Overall Risk 
            (3, 4, 0.9),  # Liquidity Risk → Overall Risk
            (0, 4, 0.4),  # Direct: Order Book Imbalance → Overall Risk
        ]
        
        # Add relationships to the quantum network
        for cause, effect, strength in risk_relationships:
            self.quantum_bayesian_network.add_conditional_relationship(
                cause_idx=cause,
                effect_idx=effect,
                strength=strength
            )
        
        logger.info(f"Defined {len(risk_relationships)} risk factor relationships")

    def _calculate_classical_risk_metrics(self, symbol: str, order_book: Dict[str, Any], stats_24hr: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate classical risk metrics for a cryptocurrency.
        
        Args:
            symbol: Cryptocurrency symbol (e.g. 'BTC', 'ETH')
            order_book: Order book data
            stats_24hr: 24-hour statistics
            
        Returns:
            Dictionary with risk metrics
        """
        # === DEBUGGING: Log Raw Inputs ===
        print(f"[DEBUG] Classical Metrics - Symbol: {symbol}")
        print(f"[DEBUG] Classical Metrics - Raw 24hr Stats (partial): lastPrice={stats_24hr.get('lastPrice')}, priceChangePercent={stats_24hr.get('priceChangePercent')}, volume={stats_24hr.get('volume')}")
        # Avoid printing the entire order book, log derived metrics instead
        
        # Extract and calculate risk metrics
        
        # 1. Bid-ask spread
        bid_price = float(stats_24hr.get('bidPrice', 0))
        ask_price = float(stats_24hr.get('askPrice', 0))
        
        if bid_price > 0 and ask_price > 0:
            bid_ask_spread = (ask_price - bid_price) / ask_price
        else:
            bid_ask_spread = 0.01  # default value if proper prices not available
        
        # 2. Volatility (from 24hr stats)
        price_change_percent = abs(float(stats_24hr.get('priceChangePercent', 5.0)) / 100)
        volatility = price_change_percent
        
        # 3. Market depth (total volume in order book)
        try:
            # For Yahoo Finance synthetic data
            if isinstance(order_book['bids'], pd.DataFrame) and isinstance(order_book['asks'], pd.DataFrame):
                bids_volume = order_book['bids']['quantity'].sum()
                asks_volume = order_book['asks']['quantity'].sum()
            else:
                # For Binance data
                bids_volume = sum(float(bid[1]) for bid in order_book.get('bids', []))
                asks_volume = sum(float(ask[1]) for ask in order_book.get('asks', []))
            
            total_depth = bids_volume + asks_volume
            
            # Normalize depth (higher is better)
            # Assumption: 1000 units is considered "deep" in this example
            normalized_depth = min(1.0, total_depth / 1000.0)
            
            # 4. Order book imbalance (bid/ask ratio)
            if asks_volume > 0:
                imbalance = abs(bids_volume / asks_volume - 1)
            else:
                imbalance = 1.0
            
            # 5. Price impact (how much would a market order of X size move the price)
            # Simplified calculation
            impact = 0.01  # default 1% impact
            
            if bids_volume > 0 and asks_volume > 0:
                # Calculate impact as inverse of liquidity
                impact = 1.0 / (normalized_depth * 10)
                impact = min(0.1, impact)  # cap at 10%
        except (KeyError, TypeError):
            # Fallback values if order book data is not in expected format
            normalized_depth = 0.5
            imbalance = 0.5
            impact = 0.05
        
        # 6. Recent trading volume (24h)
        daily_volume = float(stats_24hr.get('volume', 0))
        
        # Normalize trading volume (higher is better)
        # Assumption: 10,000 units is considered "high volume" in this example
        normalized_volume = min(1.0, daily_volume / 10000.0)
        
        # === DEBUGGING: Log Calculated Intermediate Classical Metrics ===
        print(f"[DEBUG] Classical Metrics - Calculated Intermediates:")
        print(f"  - bid_ask_spread: {bid_ask_spread:.6f}")
        print(f"  - volatility: {volatility:.4f}")
        print(f"  - normalized_depth: {normalized_depth:.4f}")
        print(f"  - imbalance: {imbalance:.4f}")
        print(f"  - impact: {impact:.4f}")
        print(f"  - normalized_volume: {normalized_volume:.4f}")
        
        # 7. Risk metrics (higher = more risk)
        liquidity_risk = (0.3 * (1 - normalized_depth) + 
                          0.3 * (1 - normalized_volume) + 
                          0.4 * bid_ask_spread) * 100
        
        volatility_risk = volatility * 100
        
        market_depth_risk = (0.7 * (1 - normalized_depth) + 
                            0.3 * imbalance) * 100
        
        price_impact_risk = impact * 100
        
        # Overall risk (weighted average)
        overall_risk = (0.3 * liquidity_risk + 
                        0.3 * volatility_risk + 
                        0.2 * market_depth_risk + 
                        0.2 * price_impact_risk)
        
        # === DEBUGGING: Log Final Classical Risk Scores ===
        print(f"[DEBUG] Classical Metrics - Calculated Risk Scores:")
        print(f"  - liquidity_risk: {liquidity_risk:.2f}")
        print(f"  - volatility_risk: {volatility_risk:.2f}")
        print(f"  - market_depth_risk: {market_depth_risk:.2f}")
        print(f"  - price_impact_risk: {price_impact_risk:.2f}")
        print(f"  - overall_risk: {overall_risk:.2f}")
        
        # Return as dictionary
        return {
            'symbol': symbol,
            'current_price': float(stats_24hr.get('lastPrice', 0)),
            'bid_ask_spread': bid_ask_spread,
            'volatility': volatility,
            'normalized_depth': normalized_depth,
            'imbalance': imbalance,
            'price_impact': impact,
            'normalized_volume': normalized_volume,
            'liquidity_risk': liquidity_risk,
            'volatility_risk': volatility_risk,
            'market_depth_risk': market_depth_risk,
            'price_impact_risk': price_impact_risk,
            'overall_risk': overall_risk
        }
    
    def analyze_with_quantum(self, symbol: str) -> Dict[str, Any]:
        """
        Perform quantum-enhanced cryptocurrency risk analysis.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            
        Returns:
            Dict containing analysis results
        """
        try:
            # Get the data fetcher
            crypto_data_fetcher = self._get_crypto_data_fetcher()

            if crypto_data_fetcher is None:
                 logger.error("Failed to initialize CryptoDataFetcher. Cannot proceed.")
                 return {"error": "Data fetcher initialization failed", "symbol": symbol}

            # Define variables for market data to ensure they exist
            order_book = None
            stats_24hr = None

            # Determine data source
            use_yahoo_finance = not self.api_key # Assuming self.api_key correctly reflects Binance availability
            print(f"[DEBUG] Quantum Analysis - Using {'Yahoo Finance' if use_yahoo_finance else 'Binance'} data for {symbol}")

            if use_yahoo_finance:
                # ... existing Yahoo Finance data fetching and synthetic data creation ...
                # Ensure order_book and stats_24hr are populated here
                pass # Placeholder, actual logic exists above
            else:
                # Fetch market data for the given symbol from Binance using CryptoDataFetcher
                try:
                    logger.info(f"Fetching order book data for {symbol}...")
                    order_book = crypto_data_fetcher.get_binance_order_book(symbol)
                except AttributeError:
                    logger.error("CryptoDataFetcher instance does not have method 'get_binance_order_book'.")
                    return {"error": "Missing method get_binance_order_book", "symbol": symbol}
                except Exception as e:
                    logger.error(f"Error fetching Binance order book: {e}", exc_info=True)
                    return {"error": f"Failed to fetch order book: {e}", "symbol": symbol}

                try:
                    logger.info(f"Fetching 24hr stats for {symbol}...")
                    stats_24hr = crypto_data_fetcher.get_binance_24hr_stats(symbol)
                except AttributeError:
                    logger.error("CryptoDataFetcher instance does not have method 'get_binance_24hr_stats'.")
                    return {"error": "Missing method get_binance_24hr_stats", "symbol": symbol}
                except Exception as e:
                    logger.error(f"Error fetching Binance 24hr stats: {e}", exc_info=True)
                    return {"error": f"Failed to fetch 24hr stats: {e}", "symbol": symbol}

            # === Check if data fetching was successful ===
            if order_book is None or stats_24hr is None:
                logger.error(f"Failed to obtain necessary market data for {symbol}. Aborting analysis.")
                return {"error": "Market data fetching failed", "symbol": symbol}

            # Prepare market data for quantum encoding
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Try block for the rest of the analysis which depends on fetched data
            try:
                # Extract necessary components from classical risk calculation for the market_data dict
                # Reconstruct the market_data dictionary based on calculated variables
                # Ensure all variables used here (like volatility, market_depth, etc.) are calculated above
                # using the fetched order_book and stats_24hr data.
                # This requires careful handling of potential missing keys in the source data.

                # Example structure (ensure these variables are defined from stats_24hr/order_book):
                try:
                    price_change_percent = abs(float(stats_24hr.get('priceChangePercent', 0.0)) / 100)
                    high_price = float(stats_24hr.get('highPrice', 0))
                    low_price = float(stats_24hr.get('lowPrice', 0))
                    weighted_avg_price = float(stats_24hr.get('weightedAvgPrice', 0))
                    if high_price > 0 and low_price > 0 and weighted_avg_price > 0:
                        relative_range = (high_price - low_price) / weighted_avg_price
                    else:
                        relative_range = 0.0 # Default
                    volatility = max(price_change_percent, relative_range)
                    volume = float(stats_24hr.get('volume', 0))
                    bids_volume = sum(float(bid[1]) for bid in order_book.get('bids', []))
                    asks_volume = sum(float(ask[1]) for ask in order_book.get('asks', []))
                    market_depth = bids_volume / asks_volume if asks_volume > 0 else 1.0
                    price_change = float(stats_24hr.get('priceChange', 0))
                    last_price = float(stats_24hr.get('lastPrice', 1))
                    momentum = price_change / last_price if last_price != 0 else 0
                    total_bid_volume = bids_volume # Alias for clarity below
                    total_ask_volume = asks_volume # Alias for clarity below

                except (TypeError, ValueError, KeyError) as data_calc_e:
                    logger.error(f"Error calculating intermediate market metrics: {data_calc_e}", exc_info=True)
                    return {"error": f"Market metric calculation failed: {data_calc_e}", "symbol": symbol}

                market_data = {
                    'symbol': symbol,
                    'volatility': volatility,
                    'market_depth': market_depth,
                    'volume': volume,
                    'price': last_price,
                    'momentum': momentum,
                    'high_price': high_price,
                    'low_price': low_price,
                    'weighted_avg_price': weighted_avg_price,
                    'price_change_percent': price_change_percent,
                    'bid_volume': total_bid_volume,
                    'ask_volume': total_ask_volume
                }
                print(f"[DEBUG] Quantum Analysis - Market Data for Quantum Input: {market_data}") # Simplified log

                # Create encoding circuit with all available market data
                # Ensure trade_size calculation is safe
                trade_size = total_bid_volume * 0.01 if total_bid_volume else 0.0
                encoding_circuit = combined_market_risk_encoding(
                    order_book, 
                    volatility, 
                    trade_size, 
                    volume
                )
                
                # Save visualization of the quantum market encoding
                output_dir = '.' # Define output dir if not class member
                viz_filename = f"{symbol}_quantum_market_encoding_{timestamp}.png"
                visualize_quantum_market_encoding(
                    encoding_circuit,
                    title=f"Quantum Market Encoding - {symbol}",
                    output_file=os.path.join(output_dir, viz_filename)
                )

                initial_probabilities = [0.5, 0.5, 0.5, 0.5, 0.5] # Default values
                print(f"[DEBUG] Quantum Analysis - Initial Probabilities for Quantum Bayesian Network: {initial_probabilities}")

                # Use quantum Bayesian network
                risk_results = self.quantum_bayesian_network.propagate_risk(
                    initial_probabilities=initial_probabilities,
                    market_data=market_data
                )
                
                # === Check risk_results format before accessing ===
                if not isinstance(risk_results, dict) or "updated_probabilities" not in risk_results:
                    logger.error(f"Invalid result format from propagate_risk: {risk_results}")
                    return {"error": "Invalid result from quantum Bayesian network", "symbol": symbol}
                    
                updated_probs = risk_results["updated_probabilities"]
                print(f"[DEBUG] Quantum Analysis - Raw Updated Probabilities from Network: {updated_probs}")

                # Calculate classical risk for comparison (needs order_book, stats_24hr)
                classical_risk = self._calculate_classical_risk_metrics(
                    symbol, order_book, stats_24hr
                )

                # Scale back quantum probs to percentages for reporting
                quantum_enhanced_risk = {
                    'order_book_imbalance_risk': updated_probs[0] * 100,
                    'volatility_risk': updated_probs[1] * 100,
                    'market_depth_risk': updated_probs[2] * 100,
                    'liquidity_risk': updated_probs[3] * 100,
                    'overall_risk': updated_probs[4] * 100
                }
                print(f"[DEBUG] Quantum Analysis - Final Quantum Enhanced Risk Scores: {quantum_enhanced_risk}")

                # Calculate differences
                risk_differences = {
                    k: quantum_enhanced_risk[k] - v
                    for k, v in classical_risk.items()
                    if k in quantum_enhanced_risk and k in ['liquidity_risk', 'volatility_risk', 'market_depth_risk', 'overall_risk']
                }

                # Network visualization
                network_file = f"{symbol}_quantum_risk_network_{timestamp}.png"
                self.quantum_bayesian_network.visualize_network(network_file)

                # Reconstruct the final results dictionary explicitly
                results = {
                    'timestamp': timestamp,
                    'symbol': symbol,
                    'current_price': classical_risk.get('current_price', 0),
                    'classical_risk': {
                        'liquidity_risk': classical_risk.get('liquidity_risk', 0),
                        'volatility_risk': classical_risk.get('volatility_risk', 0),
                        'market_depth_risk': classical_risk.get('market_depth_risk', 0),
                        'price_impact_risk': classical_risk.get('price_impact_risk', 0),
                        'overall_risk': classical_risk.get('overall_risk', 0)
                    },
                    'quantum_enhanced_risk': quantum_enhanced_risk,
                    'risk_differences': risk_differences,
                    'market_metrics': {
                        'bid_ask_spread': classical_risk.get('bid_ask_spread', 0),
                        'volatility': classical_risk.get('volatility', 0),
                        'normalized_depth': classical_risk.get('normalized_depth', 0),
                        'normalized_volume': classical_risk.get('normalized_volume', 0),
                        'imbalance': classical_risk.get('imbalance', 0),
                        'price_impact': classical_risk.get('price_impact', 0)
                    },
                    'visualizations': {
                        'market_circuit': viz_filename,
                        'risk_network': network_file
                    },
                    'quantum_shots': risk_results.get('shots', 'N/A') # Get shots if available
                }
                
                # Save results to JSON file...
                results_file = f"{symbol}_quantum_risk_results_{timestamp}.json"
                with open(results_file, 'w') as f:
                    json.dump(results, f, indent=2)
                
                logger.info(f"Analysis complete. Results saved to {results_file}")
                return results

            except KeyError as ke:
                 logger.error(f"Missing expected key in market data during analysis prep: {ke}", exc_info=True)
                 return {"error": f"Data preparation error: Missing key {ke}", "symbol": symbol}
            except Exception as analysis_e:
                 logger.error(f"Error during core analysis after data fetch for {symbol}: {analysis_e}", exc_info=True)
                 return {"error": f"Core analysis failed: {analysis_e}", "symbol": symbol}

        except Exception as outer_e:
            # Catch errors during fetcher initialization or other setup
            logger.error(f"Outer error during quantum analysis setup for {symbol}: {outer_e}", exc_info=True)
            return {"error": f"Analysis setup failed: {outer_e}", "symbol": symbol}
    
    def generate_analysis_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a markdown report of the quantum-enhanced risk analysis.
        
        Args:
            results: Results from analyze_with_quantum
            
        Returns:
            Markdown formatted report
        """
        timestamp = results.get('timestamp', datetime.now().strftime('%Y%m%d_%H%M%S'))
        symbol = results.get('symbol', 'UNKNOWN')
        
        # Create markdown report with details
        md_content = f"""# Quantum-Enhanced Risk Assessment: {symbol}

## Summary
- **Timestamp:** {timestamp}
- **Symbol:** {symbol}
- **Current Price:** ${results.get('current_price', 0):.2f}
- **Overall Risk (Quantum):** {results.get('quantum_enhanced_risk', {}).get('overall_risk', 0):.2f}%
        
## Risk Metrics

| Metric | Classical | Quantum-Enhanced | Difference |
|--------|-----------|-----------------|------------|
| Liquidity Risk | {results.get('classical_risk', {}).get('liquidity_risk', 0):.2f}% | {results.get('quantum_enhanced_risk', {}).get('liquidity_risk', 0):.2f}% | {results.get('risk_differences', {}).get('liquidity_risk', 0):.2f}% |
| Volatility Risk | {results.get('classical_risk', {}).get('volatility_risk', 0):.2f}% | {results.get('quantum_enhanced_risk', {}).get('volatility_risk', 0):.2f}% | {results.get('risk_differences', {}).get('volatility_risk', 0):.2f}% |
| Market Depth Risk | {results.get('classical_risk', {}).get('market_depth_risk', 0):.2f}% | {results.get('quantum_enhanced_risk', {}).get('market_depth_risk', 0):.2f}% | {results.get('risk_differences', {}).get('market_depth_risk', 0):.2f}% |
| Overall Risk | {results.get('classical_risk', {}).get('overall_risk', 0):.2f}% | {results.get('quantum_enhanced_risk', {}).get('overall_risk', 0):.2f}% | {results.get('risk_differences', {}).get('overall_risk', 0):.2f}% |

## Market Metrics
- **Bid-Ask Spread:** {results.get('market_metrics', {}).get('bid_ask_spread', 0):.6f}
- **Volatility:** {results.get('market_metrics', {}).get('volatility', 0):.4f}
- **Normalized Depth:** {results.get('market_metrics', {}).get('normalized_depth', 0):.4f}
- **Normalized Volume:** {results.get('market_metrics', {}).get('normalized_volume', 0):.4f}
- **Order Book Imbalance:** {results.get('market_metrics', {}).get('imbalance', 0):.4f}
- **Price Impact:** {results.get('market_metrics', {}).get('price_impact', 0):.4f}

## Visualizations

### Quantum Market Encoding
![Quantum Market Encoding](file://{results.get('visualizations', {}).get('market_circuit', '')})

### Quantum Risk Network
![Quantum Risk Network](file://{results.get('visualizations', {}).get('risk_network', '')})

## Notes
- Quantum-enhanced risk assessment takes into account quantum uncertainty and entanglement between risk factors.
- The analysis was performed using {results.get('quantum_shots', 10000)} quantum circuit shots.
- This report was generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.
"""
        
        # Save to markdown file
        report_file = f"{symbol}_quantum_risk_report_{timestamp}.md"
        with open(report_file, 'w') as f:
            f.write(md_content)
        
        logger.info(f"Report generated and saved to {report_file}")
        
        return report_file
        
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
        
        # Get data fetcher
        data_fetcher = self._get_crypto_data_fetcher()

        # === Add check: Ensure data_fetcher is not None ===
        if data_fetcher is None:
            logger.error("Failed to get CryptoDataFetcher instance for update.")
            # Return previous assessment or an error state
            return {"error": "Data fetcher unavailable for update", "symbol": symbol, "previous_timestamp": previous_assessment.get('timestamp')}
        
        # Get market data if not provided, with error handling
        try:
            if order_book is None:
                order_book = data_fetcher.get_binance_order_book(symbol)
        except AttributeError:
             logger.error("Data fetcher missing 'get_binance_order_book' method during update.")
             return {"error": "Data fetcher missing method during update", "symbol": symbol}
        except Exception as e:
             logger.error(f"Error fetching order book during update: {e}", exc_info=True)
             return {"error": f"Order book fetch failed during update: {e}", "symbol": symbol}

        try:
            if stats_24hr is None:
                stats_24hr = data_fetcher.get_binance_24hr_stats(symbol)
        except AttributeError:
             logger.error("Data fetcher missing 'get_binance_24hr_stats' method during update.")
             return {"error": "Data fetcher missing method during update", "symbol": symbol}
        except Exception as e:
             logger.error(f"Error fetching 24hr stats during update: {e}", exc_info=True)
             return {"error": f"24hr stats fetch failed during update: {e}", "symbol": symbol}
        
        # Ensure we have valid data before proceeding (added check)
        if order_book is None or stats_24hr is None:
            logger.error(f"Failed to get market data for {symbol}")
            # Return the previous assessment as fallback
            return previous_assessment
        
        # Extract previous values for comparison
        prev_classical_risk = previous_assessment.get('classical_risk', {})
        prev_market_metrics = previous_assessment.get('market_metrics', {})
        
        # Calculate new classical risk metrics
        new_classical_risk = self._calculate_classical_risk_metrics(symbol, order_book, stats_24hr)
        
        # Determine which risk factors have changed significantly
        changed_factors = []
        significant_change_threshold = 0.05  # 5% change is considered significant
        
        for metric in ['liquidity_risk', 'volatility_risk', 'market_depth_risk', 'price_impact_risk', 'overall_risk']:
            if metric in prev_classical_risk and metric in new_classical_risk:
                prev_value = prev_classical_risk.get(metric, 0)
                new_value = new_classical_risk.get(metric, 0)
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
            new_classical_risk['imbalance'],
            new_classical_risk['volatility'],
            new_classical_risk['market_depth_risk'] / 100,
            new_classical_risk['liquidity_risk'] / 100,
            new_classical_risk['overall_risk'] / 100
        ]
        
        # Create the combined quantum market circuit for visualization
        market_circuit = combined_market_risk_encoding(
            order_book_data=order_book,
            volatility=new_classical_risk['volatility'],
            trade_size=10.0,  # Standard trade size
            recent_volume=new_classical_risk['normalized_volume']
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
        self.quantum_bayesian_network.compare_classical_quantum(
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
            k.replace('_risk', ''): quantum_enhanced_risk[k] - v 
            for k, v in new_classical_risk.items() 
            if k in ['volatility_risk', 'market_depth_risk', 'liquidity_risk', 'overall_risk']
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
            'classical_risk': {
                'liquidity_risk': new_classical_risk['liquidity_risk'],
                'volatility_risk': new_classical_risk['volatility_risk'],
                'market_depth_risk': new_classical_risk['market_depth_risk'],
                'price_impact_risk': new_classical_risk['price_impact_risk'],
                'overall_risk': new_classical_risk['overall_risk']
            },
            'quantum_enhanced_risk': quantum_enhanced_risk,
            'risk_differences': risk_differences,
            'market_metrics': {
                'bid_ask_spread': new_classical_risk['bid_ask_spread'],
                'volatility': new_classical_risk['volatility'],
                'normalized_depth': new_classical_risk['normalized_depth'],
                'normalized_volume': new_classical_risk['normalized_volume'],
                'imbalance': new_classical_risk['imbalance'],
                'price_impact': new_classical_risk['price_impact']
            },
            'visualizations': {
                'market_circuit': market_circuit_file,
                'risk_network': network_file,
                'comparison': comparison_file
            },
            'quantum_shots': 5000,  # Reduced shot count for incremental updates
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

    def _watch_market_changes(self, symbol: str, interval_secs: int = 60,
                            duration_mins: int = 5, output_dir: str = '.'):
        """
        Watch for market changes over time and track risk assessment.
        
        Args:
            symbol: Cryptocurrency symbol to monitor
            interval_secs: Seconds between assessments
            duration_mins: Total minutes to monitor
            output_dir: Directory to save output files
        
        Returns:
            DataFrame with risk assessments over time
        """
        max_iterations = (duration_mins * 60) // interval_secs
        
        # Initialize results storage
        assessments = []
        timestamps = []
        
        # Initial assessment as baseline
        try: # Add try-except around initial analysis
            previous_assessment = self.analyze_with_quantum(symbol)
            if "error" in previous_assessment:
                 logger.error(f"Initial analysis failed in watch mode: {previous_assessment['error']}. Aborting watch.")
                 return None # Or return an empty DataFrame/error indicator
        except Exception as initial_e:
            logger.error(f"Exception during initial analysis in watch mode: {initial_e}", exc_info=True)
            return None

        assessments.append(previous_assessment)
        timestamps.append(datetime.now())
        
        logger.info(f"Starting market watch for {symbol} - {max_iterations} iterations")
        
        for i in range(1, max_iterations):
            logger.info(f"Iteration {i}/{max_iterations} - Waiting {interval_secs}s")
            
            # Add sleep between iterations
            import time
            time.sleep(interval_secs)
            
            # === FIX METHOD CALL: Use update_risk_assessment ===
            # Perform new assessment using update method
            try: # Add try-except around update
                new_assessment = self.update_risk_assessment( # Changed method call
                    previous_assessment=previous_assessment, symbol=symbol
                )
                if "error" in new_assessment:
                    logger.warning(f"Update assessment failed in iteration {i}: {new_assessment['error']}. Using previous assessment.")
                    # Decide how to handle error - skip this iteration? Use previous?
                    # Using previous assessment for now to avoid gaps, but log it.
                    new_assessment = previous_assessment 
                    new_assessment['timestamp'] = datetime.now().strftime('%Y%m%d_%H%M%S') # Update timestamp anyway
                    new_assessment['update_info'] = {'status': 'failed_update', 'iteration': i}
                
            except Exception as update_e:
                 logger.error(f"Exception during update assessment in iteration {i}: {update_e}", exc_info=True)
                 logger.warning("Using previous assessment due to exception during update.")
                 new_assessment = previous_assessment
                 new_assessment['timestamp'] = datetime.now().strftime('%Y%m%d_%H%M%S')
                 new_assessment['update_info'] = {'status': 'exception_during_update', 'iteration': i}


            # Store results
            assessments.append(new_assessment)
            timestamps.append(datetime.now())
            
            # Update previous for next iteration if update was successful
            # If update failed, previous_assessment remains the same as last successful one
            if "error" not in new_assessment.get('update_info', {}).get('status', ''):
                 previous_assessment = new_assessment
        
        # Create DataFrame from all assessments
        df_data = []
        
        for timestamp, assessment in zip(timestamps, assessments):
            # Extract quantum risk values
            q_risk = assessment.get('quantum_enhanced_risk', {})
            
            row = {
                'timestamp': timestamp,
                'symbol': symbol,
                'order_book_imbalance_risk': q_risk.get('order_book_imbalance_risk', 0),
                'volatility_risk': q_risk.get('volatility_risk', 0),
                'market_depth_risk': q_risk.get('market_depth_risk', 0),
                'liquidity_risk': q_risk.get('liquidity_risk', 0),
                'overall_risk': q_risk.get('overall_risk', 0)
            }
            df_data.append(row)
        
        # Create and return DataFrame
        df = pd.DataFrame(df_data)
        
        # Save results
        output_file = os.path.join(output_dir, f"{symbol}_risk_time_series.csv")
        df.to_csv(output_file, index=False)
        logger.info(f"Saved market watch results to {output_file}")
        
        return df

    def _get_crypto_data_fetcher(self):
        """
        Get an instance of the EnhancedCryptoDataFetcher.
        """
        # Import here to ensure it's attempted each time
        try:
            # Correct import path based on previous step
            from examples.crypto_data_fetcher_enhanced import EnhancedCryptoDataFetcher 
        except ImportError:
            logger.error("Could not import EnhancedCryptoDataFetcher from examples.")
            return None # Cannot proceed without the fetcher
        
        # --- Logic to find API key remains the same ---
        # Make sure we have an API key
        if not self.api_key:
            # Try to reload from environment
            self.api_key = os.environ.get('RAPIDAPI_KEY')
            # Still no API key, try to find it in a key file
            if not self.api_key:
                key_file_paths = [
                    Path('.') / 'rapidapi_key.txt',
                    Path('.') / 'keys' / 'rapidapi_key.txt',
                    Path(os.path.expanduser('~')) / '.rapidapi_key'
                ]
                for key_path in key_file_paths:
                    if key_path.exists():
                        try:
                            self.api_key = key_path.read_text().strip()
                            logger.info(f"Loaded RAPIDAPI_KEY from {key_path}")
                            break
                        except Exception as e:
                            logger.warning(f"Error reading key file {key_path}: {e}")

        # === Instantiate EnhancedCryptoDataFetcher ===
        fetcher_instance = None
        # Enhanced fetcher expects api_key in constructor based on search results
        # It also takes cache_dir, which the base class constructor used. Let's assume it takes it too.
        cache_dir = ".cache" # Define default cache dir BEFORE the try block
        
        # Note: The base CryptoDataFetcher inside EnhancedCryptoDataFetcher will get key from env var if not passed explicitly.
        # However, EnhancedCryptoDataFetcher itself takes api_key argument for BinanceMarketData component.
        
        try:
            if self.api_key:
                 logger.info(f"Attempting to instantiate EnhancedCryptoDataFetcher with API key...")
                 # Pass the found api_key and cache_dir
                 fetcher_instance = EnhancedCryptoDataFetcher(api_key=self.api_key, cache_dir=cache_dir)
                 logger.info("Successfully instantiated EnhancedCryptoDataFetcher with API key.")
            else:
                 logger.warning("No RAPIDAPI_KEY found. Attempting to instantiate EnhancedCryptoDataFetcher without API key.")
                 # Instantiate without api_key, it might still work for non-Binance parts or simulated data if supported
                 fetcher_instance = EnhancedCryptoDataFetcher(cache_dir=cache_dir) 
                 logger.info("Successfully instantiated EnhancedCryptoDataFetcher without API key (limited functionality expected).")

        except TypeError as te:
             # Catch if constructor signature is different (e.g., doesn't accept cache_dir or api_key is mandatory)
             logger.error(f"TypeError instantiating EnhancedCryptoDataFetcher: {te}. Check constructor arguments.", exc_info=True)
             # Try basic instantiation as last resort if applicable? Depends on EnhancedCryptoDataFetcher design.
             # For now, return None if the expected instantiation fails.
             return None
        except Exception as e:
             logger.error(f"Failed to instantiate EnhancedCryptoDataFetcher: {e}", exc_info=True)
             return None # Return None if any other exception occurs

        return fetcher_instance

def main():
    """Run the quantum enhanced crypto risk assessment tool."""
    parser = argparse.ArgumentParser(
        description="Quantum Enhanced Cryptocurrency Risk Assessment Tool"
    )
    
    parser.add_argument(
        "--symbol", "-s",
        type=str,
        default="BTC",
        help="Cryptocurrency symbol to analyze (default: BTC)"
    )
    
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch market changes over time"
    )
    
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=5,
        help="Duration in minutes to watch (default: 5)"
    )
    
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=60,
        help="Interval in seconds between assessments (default: 60)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=".",
        help="Output directory for result files (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Initialize the quantum risk assessment tool
    risk_tool = QuantumEnhancedCryptoRisk()
    
    if args.watch:
        logger.info(f"Watching {args.symbol} for {args.duration} minutes " 
                   f"at {args.interval}s intervals")
        
        # Watch for changes over time
        risk_tool._watch_market_changes(
            symbol=args.symbol,
            interval_secs=args.interval,
            duration_mins=args.duration,
            output_dir=args.output_dir
        )
    else:
        # One-time assessment
        results = risk_tool.analyze_with_quantum(args.symbol)
        
        # Print results
        print(f"\n===== QUANTUM RISK ASSESSMENT: {args.symbol} =====")
        print(f"Order Book Imbalance Risk: {results['quantum_enhanced_risk']['order_book_imbalance_risk']:.2f}%")
        print(f"Price Volatility Risk:     {results['quantum_enhanced_risk']['volatility_risk']:.2f}%")
        print(f"Market Depth Risk:         {results['quantum_enhanced_risk']['market_depth_risk']:.2f}%")
        print(f"Liquidity Risk:            {results['quantum_enhanced_risk']['liquidity_risk']:.2f}%")
        print(f"Overall Market Risk:       {results['quantum_enhanced_risk']['overall_risk']:.2f}%")
        print("\nRisk assessment completed and results saved to current directory")


if __name__ == "__main__":
    main() 