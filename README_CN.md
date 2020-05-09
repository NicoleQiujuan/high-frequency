# 高频跨期套利策略

[![Logo](https://img.shields.io/badge/KuCoin-KuMex-yellowgreen?style=flat-square)](https://github.com/Kucoin-academy/Guide)
[![GitHub stars](https://img.shields.io/github/stars/Kucoin-academy/simple-grid.svg?label=Stars&style=flat-square)](https://github.com/Kucoin-academy/simple-grid)
[![GitHub forks](https://img.shields.io/github/forks/Kucoin-academy/simple-grid.svg?label=Fork&style=flat-square)](https://github.com/Kucoin-academy/simple-grid)
[![GitHub issues](https://img.shields.io/github/issues/Kucoin-academy/simple-grid.svg?label=Issue&style=flat-square)](https://github.com/Kucoin-academy/simple-grid/issues)

[![](https://img.shields.io/badge/lang-English-informational.svg?longCache=true&style=flat-square)](README.md)
[![](https://img.shields.io/badge/lang-Chinese-red.svg?longCache=true&style=flat-square)](README_CN.md)

## 策略说明

交易标的：比特币（BTC）

价差数据：BTC 永续 - BTC 季度（省略协整性检验）

交易周期：1 分钟

头寸匹配：1:1

交易类型：同品种跨期

做多价差开仓条件：如果当前账户没有持仓，并且价差 < （长期价差水平 - 阈值），就做多价差。即：买开 BTC 永续，卖开 BTC 季度。

做空价差开仓条件：如果当前账户没有持仓，并且价差 > （长期价差水平 + 阈值），就做空价差。即：卖开 BTC 永续，买开 BTC 季度。

做多价差平仓条件：如果当前账户持有 BTC 永续多单，并且持有 BTC 季度空单，并且价差 > 长期价差水平，就平多价差。即：卖平 BTC 永续，买平 BTC 季度。

做空价差平仓条件：如果当前账户持有 BTC 永续空单，并且持有 BTC 季度多单，并且价差 < 长期价差水平，就平空价差。即：买平 BTC 永续，卖平 BTC 季度。

**举个例子**，假设 BTC 永续 和 BTC 当季的价差长期维持在 35 左右。如果某一天价差达到 50 ，我们预计价差会在未来某段时间回归到 35 及以下。那么就可以卖出 BTC 永续，同时买入 BTC 当季，来做空这个价差。反之亦然，注意 BTC 永续 和 BTC 当季 的价差总会回归到0附近（到期交割），所以价差为正的时候，优先做空价差，价差为负的时候，优先做多价差。



**KuCoin**拥有**level3交易数据、强大的撮合引擎、针对api用户提供的手续费折扣**，同时提供**sandbox环境**作为数据测试支撑，帮助你规避风险。

我们仅提供一个简单且不完备的交易策略，使用时**请注意规避风险**，我们希望你能够**在sandbox环境配合其他参数或是策略进行测试调整，我们也不想你成为一个慈善家！！！**

当然，如果这个过程中，你遇到任何问题或是有赚钱的策略想要分享，请在**ISSUE**中反映，我们会努力及时响应。

:point_right: 如果你对该策略有兴趣，请点击**右上角star**，我们会根据star数来衡量策略的**受欢迎程度和后续优化优先级**，你也可以点击**右上角watching**通过接收更新通知来持续关注该项目。

## 如何使用

* 安装Python

  * Windows系统请前往[Python](https://www.python.org/downloads/windows/)官网自行安装，64位请选择1，32位请选择2。

    <img src="./img/python_download.png" style="zoom:50%" />

    * 在开始安装时请注意将以下选项勾选：

      <img src="./img/python_win.png" style="zoom:40%" />

  * MAC OS X安装

    * 打开命令终端，输入以下命令安装Homebrew（安装过程中需要输入**电脑密码**）：

      ```shell
      /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
      ```

    * 在命令终端输入以下命令，安装Python3：

      ```shell
      brew install python
      ```

    * 在命令终端输入以下命令，确认是否安装成功：

      ```shell
      python3 --version
      ```

      ![](./img/python_version.gif)

* 确保你已经安装git (mac 自带该软件,终端输入`which git`，查看安装位置)，未安装者请前往官网[git](https://git-scm.com/)安装。

* 在命令终端输入以下命令，安装项目依赖：

  ```shell script
  pip3 install python-kumex
  ```

  ![pip_install](./img/pip_install.gif)
  
* 在你需要跑策略的位置新建文件夹（例如桌面），**右键**点击新建的文件夹选择“**新建位于文件夹位置的终端窗口**”（**windows**系统：在右键点击文件夹点击**git Bash here**），在弹出的窗口中输入以下命令，克隆项目至本地，完成后本地会新增文件夹**high-frequency**：
  
  ```shell
  git clone https://github.com/Kucoin-academy/high-frequency.git
  ```
  
  ![git_clone](./img/git_clone.gif)
  
* 打开克隆好的项目（**high-frequency**）文件夹，将**config.json.example**文件重命名为**config.json**，并用文本编辑器（比如**记事本**）打开**config.json**，然后完善相关的配置信息：

  ```
  {  
    "api_key": "api key",
    "api_secret": "api secret",
    "api_passphrase": "api pass phrase",
    // 是否是沙盒环境
    "is_sandbox": true,
    // 合约名称，比如：XBTUSDM
    "symbol_a": "contract name",
    // 合约名称，比如：XBTMM20
    "symbol_b": "contract name",
    // 长期价差水平，可取前三天的价差均值  
    "spread_mean": "average closed price for 3 days",
    // 价差阈值，可取前三天的价差2倍标准差左右
    "num_param": "2 * Standard deviation of spread_mean",
    // 杠杆倍数，比如：5
    "leverage": "Leverage of the order",
    // 开仓数量，比如：1
    "size": "Order size. Must be a positive number"
  }
  ```
  
* Mac/Linux **在项目目录下**打开命令终端：

  ```shell
  cd high-frequency
  ```
  * 用以下命令让你的策略运行起来：
  
    ```shell
    ./high_frequency.py
    ```
  
* Windows **在项目目录下**打开命令终端：

  ```shell
  cd high-frequency
  ```
  * 用以下命令让你的策略运行起来：
  
    ```shell
    py high_frequency.py
    ```
  
  

