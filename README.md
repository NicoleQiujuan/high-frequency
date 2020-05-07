# High-frequency intertemporal arbitrage

## Strategy description

Trading target: BTC  

Source of price spread: BTC Perpetual - BTC Quarterly (omit cointegration test)  

Trading period: 1 minute

Position ratio: 1:1  

Trading type: intertemporal arbitrage

Condition of price spread for longing: If there is no position in current account and price spread < (usual price spread - threshold), long the price spread which means long BTC Perpetual and short BTC Quarterly.  

Condition of price spread for shorting: If there is no position in current account and price spread > (usual price spread + threshold), short the price spread which means short BTC Perpetual and long BTC Quarterly.  

Condition of price spread for closing long position: If there is BTC Perpetual long position and BTC Quarterly short position, while price spread > usual price spread, close the long price spread positions, which means short to close the BTC Perpetual position and long to close the BTC Quarterly position.  

Condition of price spread for closing short position: If there is BTC Perpetual short position and BTC Quarterly long position, while price spread < usual price spread, close the short price spread positions, which means long to close the BTC Perpetual position and short to close the BTC Quarterly position.  

e.g.: If the usual price spread between BTC Perpetual and BTC Quarterly is 35. One day, the price spread rises up to 50, we predict the price spread will go back below to 35 in future. Then we could short BTC Perpetual and long BTC Quarterly to short the price spread - vice versa.  

Notice: The price spread between BTC Perpetual and BTC Quarterly will always return around to 0 (maturity date), so when the price spread is positive, short the price spread in priority, and when the price spread is negative, long the price spread in priority.  

**Moreover, KuCoin provides the transaction data of level 3, great matching engine, and the commission discount specially offers to the API customers, which could greatly reduce the disadvantages of the trading operations. At the same time, we offer the sandbox environment as the data testing support to avoid the risks.**

**Only a simple and incomplete trading strategy is provided here, so please pay attention to avoiding risks when using it. Of course, we do not want you to suffer more losses, so please do not directly run it in the actual environment before you have tested it yourself. We do not want you to become a philanthropist! ! !**

**If you want to use the strategy in the actual environment to earn stable profits, we hope that you can make test adjustments in the sandbox environment with other parameters or strategies to enable you to achieve your goals. We also look forward to sharing your test data and Insights.**

**Surely, if you encounter any problems in this process, or you have a profitable strategy to share, please reflect in ISSUE, we will try to respond in a timely manner.**  

**If you are interested in this strategy, please click the star in the upper right corner, we will  measure the popularity of this strategy and subsequent optimization priorities based on the amounts of stars. You can also click watching in the upper right corner to continue to follow this project by receiving update notifications**.  

## How to use

* After clone this project to your local, install the dependency: 

  ```shell script
  pip install python-kumex
  ```

* Paste config.json.example,  rename as config.json, then add the relevant configuration information:  

  ```
  {  
    "api_key": "api key",
    "api_secret": "api secret",
    "api_passphrase": "api pass phrase",
    //  if sandbox
    "is_sandbox": true,
    // contract name, e.g.: XBTUSDM
    "symbol_a": "contract name",
    // contract name, e.g.: XBTMM20
    "symbol_b": "contract name",
    // usual price spread, good as the average price of the past 3 days price spread  
    "spread_mean": "average closed price for 3 days",
    // price spread threshold, good as 2 times of the standard deviation of the past 3 days price spread
    "num_param": "2 * Standard deviation of spread_mean",
    // leverage, e.g.:5
    "leverage": "Leverage of the order",
    // order size, e.g.: 1
    "size": "Order size. Must be a positive number"
  }
  ```

  

* Run your strategy

  ```shell
  ./high_frequency.py
  ```

  