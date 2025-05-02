# compass_api_sdk

Developer-friendly & type-safe Python SDK specifically catered to leverage *compass_api_sdk* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=compass-api-sdk&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<br /><br />
> [!IMPORTANT]
> This SDK is not yet ready for production use. To complete setup please follow the steps outlined in your [workspace](https://app.speakeasy.com/org/compasslabs/api). Delete this section before > publishing to a package manager.

<!-- Start Summary [summary] -->
## Summary

Compass API: Compass Labs DeFi API
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [compass_api_sdk](#compassapisdk)
  * [SDK Installation](#sdk-installation)
  * [IDE Support](#ide-support)
  * [SDK Example Usage](#sdk-example-usage)
  * [Authentication](#authentication)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Resource Management](#resource-management)
  * [Debugging](#debugging)
* [Development](#development)
  * [Maturity](#maturity)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install compass_api_sdk
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add compass_api_sdk
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from compass_api_sdk python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "compass_api_sdk",
# ]
# ///

from compass_api_sdk import CompassAPISDK

sdk = CompassAPISDK(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from compass_api_sdk import CompassAPISDK, models


with CompassAPISDK(
    api_key_auth="<YOUR_API_KEY_HERE>",
) as cas_client:

    res = cas_client.aave_v3.token_price(chain=models.AaveTokenPriceChain.ARBITRUM_MAINNET, token=models.AaveTokenPriceToken.USDC)

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from compass_api_sdk import CompassAPISDK, models

async def main():

    async with CompassAPISDK(
        api_key_auth="<YOUR_API_KEY_HERE>",
    ) as cas_client:

        res = await cas_client.aave_v3.token_price_async(chain=models.AaveTokenPriceChain.ARBITRUM_MAINNET, token=models.AaveTokenPriceToken.USDC)

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name           | Type   | Scheme  |
| -------------- | ------ | ------- |
| `api_key_auth` | apiKey | API key |

To authenticate with the API the `api_key_auth` parameter must be set when initializing the SDK client instance. For example:
```python
from compass_api_sdk import CompassAPISDK, models


with CompassAPISDK(
    api_key_auth="<YOUR_API_KEY_HERE>",
) as cas_client:

    res = cas_client.aave_v3.token_price(chain=models.AaveTokenPriceChain.ARBITRUM_MAINNET, token=models.AaveTokenPriceToken.USDC)

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [aave_v3](docs/sdks/aavev3/README.md)

* [token_price](docs/sdks/aavev3/README.md#token_price) - Token prices
* [liquidity_change](docs/sdks/aavev3/README.md#liquidity_change) - Liquidity index
* [user_position_summary](docs/sdks/aavev3/README.md#user_position_summary) - Positions - total
* [user_position_per_token](docs/sdks/aavev3/README.md#user_position_per_token) - Positions - per token
* [supply](docs/sdks/aavev3/README.md#supply) - Supply/Lend
* [borrow](docs/sdks/aavev3/README.md#borrow) - Borrow
* [repay](docs/sdks/aavev3/README.md#repay) - Repay loans
* [withdraw](docs/sdks/aavev3/README.md#withdraw) - Unstake

### [aerodrome_slipstream](docs/sdks/aerodromeslipstream/README.md)

* [slipstream_liquidity_provision_positions](docs/sdks/aerodromeslipstream/README.md#slipstream_liquidity_provision_positions) - List LP positions
* [slipstream_pool_price](docs/sdks/aerodromeslipstream/README.md#slipstream_pool_price) - Pool price
* [slipstream_swap_sell_exactly](docs/sdks/aerodromeslipstream/README.md#slipstream_swap_sell_exactly) - Swap - from specified amount
* [slipstream_swap_buy_exactly](docs/sdks/aerodromeslipstream/README.md#slipstream_swap_buy_exactly) - Swap - into specified amount
* [slipstream_liquidity_provision_mint](docs/sdks/aerodromeslipstream/README.md#slipstream_liquidity_provision_mint) - Open a new LP position
* [slipstream_liquidity_provision_increase](docs/sdks/aerodromeslipstream/README.md#slipstream_liquidity_provision_increase) - Increase an LP position
* [slipstream_liquidity_provision_withdraw](docs/sdks/aerodromeslipstream/README.md#slipstream_liquidity_provision_withdraw) - Withdraw an LP position


### [morpho](docs/sdks/morpho/README.md)

* [vaults](docs/sdks/morpho/README.md#vaults) - Get Vaults
* [vault_position](docs/sdks/morpho/README.md#vault_position) - Check Vault Position
* [markets](docs/sdks/morpho/README.md#markets) - Get Markets
* [market_position](docs/sdks/morpho/README.md#market_position) - Check Market Position
* [allowance](docs/sdks/morpho/README.md#allowance) - Set Allowance for Vault
* [deposit](docs/sdks/morpho/README.md#deposit) - Deposit to Vault
* [withdraw](docs/sdks/morpho/README.md#withdraw) - Withdraw from Vault
* [supply_collateral](docs/sdks/morpho/README.md#supply_collateral) - Supply Collateral to Market
* [withdraw_collateral](docs/sdks/morpho/README.md#withdraw_collateral) - Withdraw Collateral from Market
* [borrow](docs/sdks/morpho/README.md#borrow) - Borrow from Market
* [repay](docs/sdks/morpho/README.md#repay) - Repay to Market

### [token](docs/sdks/tokensdk/README.md)

* [address](docs/sdks/tokensdk/README.md#address) - Token Address
* [price](docs/sdks/tokensdk/README.md#price) - Token Price
* [balance](docs/sdks/tokensdk/README.md#balance) - Token Balance
* [transfer](docs/sdks/tokensdk/README.md#transfer) - Transfer ETH or ERC20 Tokens

### [uniswap_v3](docs/sdks/uniswapv3/README.md)

* [quote_buy_exactly](docs/sdks/uniswapv3/README.md#quote_buy_exactly) - Get quote - to specified amount
* [quote_sell_exactly](docs/sdks/uniswapv3/README.md#quote_sell_exactly) - Get quote - from specified amount
* [pool_price](docs/sdks/uniswapv3/README.md#pool_price) - Pool price
* [liquidity_provision_in_range](docs/sdks/uniswapv3/README.md#liquidity_provision_in_range) - Check if LP is active.
* [liquidity_provision_positions](docs/sdks/uniswapv3/README.md#liquidity_provision_positions) - List LP
* [swap_buy_exactly](docs/sdks/uniswapv3/README.md#swap_buy_exactly) - Buy exact amount
* [swap_sell_exactly](docs/sdks/uniswapv3/README.md#swap_sell_exactly) - Sell exact amount
* [liquidity_provision_increase](docs/sdks/uniswapv3/README.md#liquidity_provision_increase) - Increase an LP position
* [liquidity_provision_mint](docs/sdks/uniswapv3/README.md#liquidity_provision_mint) - Open a new LP position
* [liquidity_provision_withdraw](docs/sdks/uniswapv3/README.md#liquidity_provision_withdraw) - Withdraw an LP position

### [universal](docs/sdks/universal/README.md)

* [portfolio](docs/sdks/universal/README.md#portfolio) - List user portfolio
* [visualize_portfolio](docs/sdks/universal/README.md#visualize_portfolio) - Visualize user portfolio
* [price_usd](docs/sdks/universal/README.md#price_usd) - Token price
* [supported_tokens](docs/sdks/universal/README.md#supported_tokens) - List supported tokens
* [balance](docs/sdks/universal/README.md#balance) - User Token Balance
* [allowance](docs/sdks/universal/README.md#allowance) - Get allowance - Protocol
* [ens](docs/sdks/universal/README.md#ens) - Resolve ENS
* [wrap_eth](docs/sdks/universal/README.md#wrap_eth) - Wrap ETH
* [unwrap_weth](docs/sdks/universal/README.md#unwrap_weth) - Unwrap WETH
* [transfer_erc20](docs/sdks/universal/README.md#transfer_erc20) - Transfer Token
* [transfer_native_token](docs/sdks/universal/README.md#transfer_native_token) - Transfer ETH
* [allowance_set](docs/sdks/universal/README.md#allowance_set) - Set Allowance - Protocol

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from compass_api_sdk import CompassAPISDK, models
from compass_api_sdk.utils import BackoffStrategy, RetryConfig


with CompassAPISDK(
    api_key_auth="<YOUR_API_KEY_HERE>",
) as cas_client:

    res = cas_client.aave_v3.token_price(chain=models.AaveTokenPriceChain.ARBITRUM_MAINNET, token=models.AaveTokenPriceToken.USDC,
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from compass_api_sdk import CompassAPISDK, models
from compass_api_sdk.utils import BackoffStrategy, RetryConfig


with CompassAPISDK(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key_auth="<YOUR_API_KEY_HERE>",
) as cas_client:

    res = cas_client.aave_v3.token_price(chain=models.AaveTokenPriceChain.ARBITRUM_MAINNET, token=models.AaveTokenPriceToken.USDC)

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a errors.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `token_price_async` method may raise the following exceptions:

| Error Type                 | Status Code | Content Type     |
| -------------------------- | ----------- | ---------------- |
| errors.HTTPValidationError | 422         | application/json |
| errors.APIError            | 4XX, 5XX    | \*/\*            |

### Example

```python
from compass_api_sdk import CompassAPISDK, errors, models


with CompassAPISDK(
    api_key_auth="<YOUR_API_KEY_HERE>",
) as cas_client:
    res = None
    try:

        res = cas_client.aave_v3.token_price(chain=models.AaveTokenPriceChain.ARBITRUM_MAINNET, token=models.AaveTokenPriceToken.USDC)

        # Handle response
        print(res)

    except errors.HTTPValidationError as e:
        # handle e.data: errors.HTTPValidationErrorData
        raise(e)
    except errors.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from compass_api_sdk import CompassAPISDK, models


with CompassAPISDK(
    server_url="https://api.compasslabs.ai",
    api_key_auth="<YOUR_API_KEY_HERE>",
) as cas_client:

    res = cas_client.aave_v3.token_price(chain=models.AaveTokenPriceChain.ARBITRUM_MAINNET, token=models.AaveTokenPriceToken.USDC)

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from compass_api_sdk import CompassAPISDK
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = CompassAPISDK(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from compass_api_sdk import CompassAPISDK
from compass_api_sdk.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = CompassAPISDK(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `CompassAPISDK` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
from compass_api_sdk import CompassAPISDK
def main():

    with CompassAPISDK(
        api_key_auth="<YOUR_API_KEY_HERE>",
    ) as cas_client:
        # Rest of application here...


# Or when using async:
async def amain():

    async with CompassAPISDK(
        api_key_auth="<YOUR_API_KEY_HERE>",
    ) as cas_client:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from compass_api_sdk import CompassAPISDK
import logging

logging.basicConfig(level=logging.DEBUG)
s = CompassAPISDK(debug_logger=logging.getLogger("compass_api_sdk"))
```
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=compass-api-sdk&utm_campaign=python)
