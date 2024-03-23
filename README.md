# TradeWiSE

[![hackmd-github-sync-badge](https://hackmd.io/1wmKYf4ZTs-fwh1vofwCOQ/badge)](https://hackmd.io/1wmKYf4ZTs-fwh1vofwCOQ)

![DALL·E 2023-12-02 00.04.25 - A sleek and modern logo for a financial technology service named 'TradeWiSE'. The logo should embody elements that represent trading and wisdom, like ](./images/logo-1280x640.png)

## About TradeWiSE: A Chatbot for Smarter TWSE Investing
TradeWiSE is a compact and sophisticated chatbot. It aims to semi-automate the investment process in the Taiwan Stock Exchange (TWSE), catering to those with busy lifestyles who wish to maintain their investments. The design allows for easy integration of customized analysis techniques and collaborative development of common features under an open-source license. Each instance is tailored for personal use, making it ideal for users with some development skills.

TradeWiSE 是一款小型聊天機器人。目的在半自動化台灣證券交易所（TWSE）的投資過程，適合忙碌生活中希望維持投資的人士。設計上允許協作者輕鬆加入客製化分析方法，並且可以在開源授權下與他人共同開發其他通用功能。每個實例都是為個人使用設計，適合具有一定開發能力的用戶。

### Core Features (and More on the Horizon)
* Automated Financial Analysis: Executes collaborator-customized strategies, automatically calculating targeted financial metrics.
    * 自動財務分析：執行協作者客製化的策略，自動計算關注的財務指標。
* Market Tracking: Continuously monitors your selected companies and automatically executes trades at optimal times.
    * 市場追蹤：持續追蹤關注的公司，並在合適的時機自動執行交易。
* Timely Reminders: Alerts users to review specific holdings and assists in calculating annualized returns.
    * 定時提醒：提醒使用者檢視特定持股，並協助計算年化報酬率。

### Technology Stack and Frameworks
In this project, we've employed a range of technologies and tools for the development, deployment, and maintenance of the system. These technologies include:

在此專案中，我們採用了一系列的技術和工具，以實作系統的開發、部署和運維。這些技術包括：

* Docker: As our primary containerization platform, Docker is used for packaging and deploying various services. It provides a consistent and portable environment for our services, making deployment and maintenance more straightforward.
    * Docker：作為主要的容器化平台，Docker 被用於封裝和部署各個服務。它為我們的服務提供了一致和可移植的環境，使部署和維護變得更加容易。
* Git: Git is our version control system, aiding in managing the project's change history and supporting collaborative development.
    * Git：Git 是我們的版本控制系統，它幫助我們管理專案的變更歷史，並支持多人協作開發。

Built on these core technologies, our services may choose different languages and frameworks according to their specific needs, including but not limited to:

在這些核心技術的基礎上，我們的各個服務可能會選擇使用不同的語言和框架，具體包括但不限於：

* Python: Many services opt for Python as their programming language, especially those involving data processing and analysis.
    * Python：許多服務選擇 Python 作為開發語言，特別是那些涉及到資料處理和分析的服務。
* FastAPI: For services requiring high-performance APIs, FastAPI is a popular choice. Renowned for its speed, simplicity, and ease of use, it's well-suited for the rapid development of modern web applications.
    * FastAPI：對於需要高性能 API 的服務，FastAPI 是一個常用選擇。它以其快速、簡潔且易於使用的特性而著稱，適合快速開發現代 Web 應用程序。

Furthermore, services in the project may select appropriate technologies and tools based on their individual requirements and characteristics. This flexibility allows us to choose the most suitable solutions for different problems.

此外，專案中的服務可能會根據各自的需求和特點選擇適合的技術和工具，這種靈活性使得我們能夠針對不同的問題選擇最合適的解決方案。

### Jump In, Let's Collaborate:
* If stocks and coding are your things, or just looking for a casual project, you're welcome to join us. There's always room for new ideas and enhancements!
    * 如果對股票、程式設計感興趣，都歡迎加入我們，這只是一個休閒的小專案。
* We embrace the Mozilla license for broad collaboration, ensuring open contribution. However, for those concerned about disclosing their strategies, the key strategic components are under the MIT license.
    * 我們採用 Mozilla 授權以促進廣泛合作，確保開放的貢獻。然而，對於那些擔心策略外洩的人，關鍵策略部分則採用 MIT 授權。
* Peek at the [dev-docs](./dev-docs) for the nitty-gritty on how TradeWiSE works.
    * 看看 [dev-docs](./dev-docs)，了解 TradeWiSE 的運作細節。

## License
This project, TradeWiSE, is primarily licensed under the Mozilla Public License 2.0 (MPL 2.0). This license grants freedoms for the use, modification, and sharing of the code while requiring that any modifications be distributed under the same license.

### Main Project License
All code in this project, except for the service specifically mentioned below, is released under the Mozilla Public License 2.0. You can find the complete license agreement for the majority of the project in the root directory of this project.

### Special Service License - insight-engine
The insight-engine service within this project is licensed under the MIT License. This is a more permissive license that allows users to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the service with minimal restrictions.

The specific terms of the MIT License for the insight-engine service can be found in the LICENSE file within its directory.

The rationale behind using different licenses in this project is to accommodate varying degrees of openness and reuse within its components. The MPL 2.0 license, used for the majority of the project, ensures that modifications to the code remain open. However, for the insight-engine service, which involves strategies and methods that individuals might want to modify more freely, the MIT license offers the necessary flexibility. This allows contributors and users of the insight-engine service to adapt and use the code with fewer restrictions, fostering innovation and broader use in diverse contexts.

### Note to Contributors

All contributions to the TradeWiSE project, regardless of size, are considered to be released under the Mozilla Public License 2.0, unless specified otherwise. Contributions to the insight-engine service should adhere to the MIT License.

## Maintenance
[GitHub Repository](https://github.com/Rezztech/TradeWiSE)
