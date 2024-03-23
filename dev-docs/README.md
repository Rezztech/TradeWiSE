# DEVELOPER GUIDE

[![hackmd-github-sync-badge](https://hackmd.io/ma7sZTGtQCmuZeVlDfBA-A/badge)](https://hackmd.io/ma7sZTGtQCmuZeVlDfBA-A)

## Project Structure and Architecture
### Microservices Details（微服務詳情）
#### Telegram 聊天機器人 `telegram-bot`
用戶與系統互動的第一接觸點，透過 Telegram 機器人提供直接且客製化的用戶體驗。它的主要功能包括：
* 即時通訊互動：用戶可以透過 Telegram 機器人發送指令，例如查詢股票價格、設置股票監控條件等。機器人會即時解析這些指令並給予相對應的反饋或動作。
* 股票價格提醒：當用戶關注的股票出現顯著價格波動時，機器人會主動發送提醒給用戶。這使得用戶可以快速做出交易決策或進行市場分析。
* 定時提醒功能：用戶可以設定定時提醒，以定期檢查關注股票的表現或公司新聞，幫助用戶保持對市場動態的持續關注。
* 個人化服務設計：每個 Telegram 機器人實例被設計為服務單一用戶，從而確保了服務的客製化和隱私保護。


#### 報告蒐集服務 `report-harvester`
專注於從多個來源自動蒐集和處理財務及市場相關的報告。它的主要職責和功能包括：
* 自動化數據蒐集：這個服務定期從不同的資料來源，如 mops-crawler，自動蒐集財務報告和市場資料。這種自動化過程確保了資料的及時性和完整性，並減少了手動工作的需要。
* 與資料庫的接口：`report-harvester` 負責將處理好的資料傳輸到中央資料庫，例如 `database-api`。這確保了所有收集的資料都能被儲存和檢索，用於後續的分析和決策。
* 定期更新和維護：服務設計了機制以定期更新資料，並確保資料的時效性。此外，定期檢查和維護確保服務穩定運行，並及時處理任何潛在的問題。
* 數據整合與處理：收集到的資料被整合和格式化，使之適用於進一步的分析。

#### 報告分析服務 `insight-engine`
設計為讓協作者能夠靈活客製財務分析方法的框架。其核心特點和規劃包括：
* 靈活的分析方法整合：此框架計劃實作的是一個可輕易整合不同協作者開發的財務分析方法。這樣的設計允許協作者根據自己的需求和偏好，添加或修改分析算法。
* 運行時算法切換：將實作在運行時切換不同的分析算法，讓協作者能夠根據當前的分析需求選擇最合適的方法。
* 共享與隱私的平衡：採用 MIT 授權的這個框架，旨在促進分析方法的共享和創新，同時保護那些不願公開自己投資決策方法的協作者的隱私。

另外還有與個人的財務分析更相關的功能，例如：
* 投資分析提醒：提醒使用者進行定期的投資分析。這意味著當到達特定時間點或市場條件變化時，它會通知使用者檢視和重新評估其庫存中的企業。
* 庫存管理與損益追蹤：考慮到它能夠訪問 `fugle-trading` 中的個人交易資料，他還提供相關的財務指標分析。例如計算和展示個別股票和整體投資組合的年化報酬率。

#### MOPS 爬蟲機器人 `mops-crawler`
設計用於從台灣證券交易所公開資訊觀測站抓取財務數據的服務。它的主要功能和特點包括：
* 遵守資料來源限制：為了避免違反網站政策或觸發防爬機制，實作了速率限制功能。這確保了資料抓取過程穩定。
* 資料消毒和預處理：抓取的資料經過初步的消毒，去除無效或不相關的資料，以便於後續的處理和分析。

#### 交易處理服務 `order-manager`
設計用於管理和執行股票交易的服務。它在整個交易系統中扮演著關鍵角色，主要功能和特點包括：
* 自動化交易邏輯：這個服務能夠基於預設的策略和規則自動執行交易。這包括根據特定的市場條件或價格觸發點自動買賣股票。
* 實時市場監控：實時監控股市動態，確保交易策略可以迅速響應市場變化。

#### 富果行情轉接頭 `fugle-market-data`
作為一個轉接頭（adapter），連接富果股市行情的 API，標準化股票市場資料的獲取過程。它的核心職能是：
* 實時行情提取：從富果行情 API 獲取即時的股票價格和交易訊息。
* 資料格式統一：將獲取的數據轉換為統一格式，方便系統內部其他服務進行處理和分析。

#### 富果交易轉接頭 `fugle-trading`
作為連接富果交易平台的轉接頭（adapter），專門處理交易執行和資料整合
* 交易執行：這個服務使系統能夠直接與富果交易 API 連接，從而執行購買和銷售股票等交易指令。
* 安全性和加密：鑒於交易的敏感性和安全需求，特別強調安全性措施，包括 API 密鑰管理和，以保護交易過程。
* 個人庫存資料同步：該服務負責將交易紀錄和相關資料與用戶的個人庫存資料進行串接，確保用戶能夠即時追蹤並管理其投資組合。

#### 資料庫 `database` `database-api`
* `database` 是系統中的關鍵資料儲存服務，通常採用直接從 SQL 提供的 Docker Image 來部署。
* `database-api`：提供一個簡單的介面，允許系統內的其他服務訪問和變更儲存在 `database` 中的資料。

#### 通知和日誌 `logging`
負責日誌記錄和錯誤通知的關鍵服務。它的主要功能包括：
* 錯誤跟蹤和通知：當系統中發生錯誤或異常時，捕捉這些事件並透過電子郵件或其他通知系統及時通知系統管理員或開發團隊。
* 日誌記錄：這個服務記錄系統的詳細日誌，包括用戶的請求、系統的回應以及任何重要的系統事件。

### Service Interactions and Data Flow（服務互動和資料流）
#### Data Collection and Integration Group（資料蒐集和整合群組）
* 涉及的服務：`mops-crawler`, `report-harvester`, `database-api`
* 描述：這個群組負責從外部來源蒐集財務報告（`mops-crawler`），加工和整合這些資料（`report-harvester`），並將它們儲存到資料庫中（`database-api`）。
* [Link](./DataCollectionAndIntegrationGroup.md)
#### Trading Strategy and Execution Group（交易策略和執行群組）
* 涉及的服務：`fugle-market-data`, `fugle-trading`, `order-manager`, `database-api`
* 描述：這個群組專注於實時市場數據的獲取（`fugle-market-data`），執行交易操作（`fugle-trading` 和 `order-manager`），並紀錄資料於資料庫（`database-api`）。
* [Link](./TradingStrategyAndExecutionGroup.md)

#### Financial Analysis Group（財務分析群組）
* 涉及的服務：`insight-engine`, `database-api`, `fugle-trading`, `fugle-market-data`
* 描述：這個群組從資料庫中取得財務資料（`database-api`）和利用市場數據（`fugle-trading` 和 `fugle-market-data`），進行客製化分析（`insight-engine`）。
* [Link](./FinancialAnalysisGroup.md)

#### User Interaction and Communication Group（用戶互動和通訊群組）
* 涉及的服務：`telegram-bot`，以及其與其他服務的互動，如 `database-api`, `order-manager`, `insight-engine`
* 描述：這個群組專注於用戶與系統之間的直接互動（`telegram-bot`），包括接收用戶指令和提供反饋，以及與其他服務的資料交換和指令執行。
* [Link](./UserInteractionAndCommunicationGroup.md)

## Environment Setup and Configuration

To set up the TradeWiSE application, you need to configure several services, each potentially requiring unique configuration files and environment variables. This document guides you through setting up the configuration for the fugle-trading service as an example.

### Configuring the fugle-trading Service
The fugle-trading service requires a configuration file (config.fugletrading.ini) and a certificate file (cert.p12).

Steps:
* Initial Setup:
    * Navigate to the config-example directory in the TradeWiSE project.
    * You will find config.fugletrading.ini.example and cert.p12.example.

* Create Actual Config Files:
    * Copy config.fugletrading.ini.example and cert.p12.example from the config-example directory to the config directory.
    * Rename config.fugletrading.ini.example to config.fugletrading.ini.
    * Rename cert.p12.example to cert.p12.

* Edit the Configuration File:
    * Open config.fugletrading.ini in a text editor.
    * Fill in the actual values for API keys, secrets, and other configurations as needed.
    * Ensure the certificate path in config.fugletrading.ini points to /app/cert.p12.

### Environment Variables:
If the service requires environment variables (e.g., for the Telegram bot), you need to set these up in a .env file located in the config directory.

### Running the Services:
With the configurations in place, you can start the services using Docker Compose:

```
docker-compose up -d
```

This command will launch all services defined in your docker-compose.yml, applying the configurations you've set up.

Note: For production environments, ensure the security of your configuration files, especially those containing sensitive information like API keys or certificates.


## Code Style and Development Standards (Optional)
### Coding conventions
- [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks):
  - `trailing-whitespace`: Trims trailing whitespace
  - `end-of-file-fixer`: Ensures files end with a newline

- [isort](https://github.com/PyCQA/isort):
  - `isort`: Sorts import statements according to the isort configuration

Some basic Python conventions:
- Use descriptive names (no abbreviations) for variables, functions, classes, etc.
- Follow the `lowercase_with_underscores` style for functions/variables
- Use `CapitalizedWords` for class names
- Indent and space your code properly for readability
- Add docstrings to document your code

### Standards for code commenting and documentation.
#### Docstrings
- All public functions, classes, and modules should have docstrings following the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Docstrings should describe the purpose, parameters, return values, and any exceptions raised
- Example usage can be included for complex functions/classes

#### Comments
- Use comments sparingly - strive to write self-documenting code
- Comments should explain the "why" behind the code, not the "what" (which should be self-evident)

#### Documentation
- Keep important design decisions documented, e.g., in a DESIGN.md file

### Standards for commits and merge requests
We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for commit messages. This lightweight convention provides an easy set of rules for creating an explicit commit history, which makes it easier to write automated tools on top of it. The commit message should be structured as follows:
```
<type>[optional scope]: <description>
[optional body]
[optional footer(s)]
```
The commit `type` can be one of the following:

- `fix`: a commit that patches a bug
- `feat`: a commit that introduces a new feature
- `BREAKING CHANGE`: a commit that introduces a breaking API change (can be part of any type)
- Other types like `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`, etc.

The commit message should clearly describe the changes made, and breaking changes should be indicated by appending `!` after the type or by including a `BREAKING CHANGE` footer.

For more details and examples, refer to the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Development Process and Workflow
* Description of development, testing, and deployment processes.
* Version control system used and its workflow.
* How to report issues and request features.

## Build and Deployment Guide
This section deals with how to take the code from the development stage to a stage where it is ready for use, either for testing or production. It includes:

* Building the Project: Instructions on how to compile or build the project, which might involve compiling code, bundling assets, or preparing the application for deployment.
* Deployment Steps: Detailed steps or scripts used to deploy the project to a testing, staging, or production environment. This might include instructions on deploying to cloud platforms, setting up CI/CD pipelines, or using containerization technologies like Docker.
* Deployment Strategies: Information on different deployment strategies (like blue-green deployment, canary releases) if used in the project.
* Post-Deployment Configuration: Details on any configuration or steps required after deployment, such as database migrations, cache invalidation, or setting environment variables in the production environment.

## Testing Strategy
### API Endpoint Tests
We use GitHub Actions to run automated tests for our API endpoints on every push and pull request. The tests are executed within Docker containers, ensuring a consistent and isolated testing environment.

The workflow is defined in `.github/workflows/api-tests.yml` and includes the following steps:

1. Checkout the repository
2. Start the required services using `docker-compose -f docker-compose.test.yml up -d`
3. Run the tests with `docker-compose -f docker-compose.test.yml run test`
4. Stop the services with `docker-compose -f docker-compose.test.yml down`

#### Running Tests Locally
To run the API endpoint tests locally, you'll need to have Docker and Docker Compose installed. Then, you can use the following commands:

```bash
# Start the required services
docker-compose -f docker-compose.test.yml up -d

# Run the tests
docker-compose -f docker-compose.test.yml run test

# Stop the services
docker-compose -f docker-compose.test.yml down
```

#### Writing Tests
[Explain any conventions, best practices, or guidelines for writing new API endpoint tests in your project.]

#### Code Coverage
[If applicable, describe how you measure and track code coverage for your API endpoint tests.]

#### Test Maintenance
[Discuss any processes or practices you follow to keep your API endpoint tests up-to-date and maintainable as the codebase evolves.]

## Appendix and Reference Materials
* [Day 02 - 數據即財富：股市資料來源與取得 ](https://ithelp.ithome.com.tw/articles/10287328)
* [GitHub - Topic - TWSE](https://github.com/topics/twse)
* [元大 API](http://easywin.yuantafutures.com.tw/api/download.html)
* [FinMind - 製作個人專屬看盤軟體（二）](https://medium.com/finmind/%E8%A3%BD%E4%BD%9C%E5%80%8B%E4%BA%BA%E5%B0%88%E5%B1%AC%E7%9C%8B%E7%9B%A4%E8%BB%9F%E9%AB%94-%E4%BA%8C-27081ce44689)
