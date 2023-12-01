# TradeWiSE
###### tags: `financial` `stock`

## Microservices

#### Telegram Bot 服務
* 負責處理與使用者的互動，如接收指令和發送回應。
* 透過 API 或訊息佇列與其他服務溝通。
* 股票價格提醒: 當庫存或關注的股票出現大波動時，通過 Telegram 發送提醒。
* 定時提醒: 定時提醒檢查庫存企業的狀況。

#### TWSE 財務資料服務
* 從 TWSE API 取得公司的財務報表資料。

#### 股票行情資料服務
* 與券商行情 API 互動，取得股票價格和交易資訊。
* 提供股票價格和交易資訊的查詢功能。

#### 股票交易服務
* 與券商交易 API 互動，執行下單服務。
* 安全性: 考慮實現例如 API 密鑰管理、加密通訊等安全措施。

#### 交易處理服務
* 負責處理股票買賣的具體邏輯，例如自動下單、監控指定價格等。

#### 資料分析服務
* 分析財務報表，識別長期穩定盈利的企業。
* 可進行複雜的資料分析和處理，支援決策制定。

#### 資料庫服務
* 管理資料儲存，例如財務報表、股票交易資料等。
* 提供資料的持久化和查詢功能。

#### 通知和日誌服務
* 負責系統的錯誤通知和日誌記錄。
* 透過電子郵件發送錯誤通知，並管理日誌儲存。

## 測試與部署
- 單元測試: 對關鍵功能進行單元測試，確保穩定性和可靠性。
- 部署: 在家中的伺服器上部署此機器人。

## Note
- 數據一致性: 確保從不同來源獲取的數據之間的一致性和準確性。
- 安全措施: 特別是處理交易命令時，需要實現足夠的安全機制。例如，可以考慮實施交易密碼確認、加密存儲 API 密鑰等措施。
- 回報新聞: 將來可以考慮添加一個功能，用於回報與關注股票相關的重要新聞。
- 股價合理性分析: 之後可以實現股票應有價格的計算功能，輔助做出更精準的投資決策。

## Reference
### Packages


* [台灣證券交易所 - 簽約資訊公司名冊](https://www.twse.com.tw/zh/products/information/list.html)
* [台灣證券交易所 - 公開資訊觀測站](https://mops.twse.com.tw/mops/web/index)
* [台灣證券交易所 - OpenAPI](https://openapi.twse.com.tw/)


- [Fugle Trading API Key](https://fugletradingapi.esunsec.com.tw/keys/apikey/APIKeyManagement)
- [Fugle Trading API Docs](https://developer.fugle.tw/docs/trading/intro/)
- [Fugle Data API Key](https://developer.fugle.tw/docs/key/)
- [Fugle Data API Docs](https://developer.fugle.tw/docs/data/intro)

### Other
* [GitHub - Topic - TWSE](https://github.com/topics/twse)
* [元大 API](http://easywin.yuantafutures.com.tw/api/download.html)
* [twstock github](https://github.com/mlouielu/twstock)

