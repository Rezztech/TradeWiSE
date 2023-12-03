# TradeWiSE
###### tags: `financial` `stock`
![DALL·E 2023-12-02 00.04.25 - A sleek and modern logo for a financial technology service named 'TradeWiSE'. The logo should embody elements that represent trading and wisdom, like ](./images/logo.png)

## About TradeWiSE: A Chatbot for Smarter TWSE Investing
TradeWiSE, a neat little chatbot I've been tinkering with. It's all about making investing in the Taiwan Stock Exchange (TWSE) a tad easier and more insightful.

### Core Features (and More on the Horizon)
* Simplified Financial Analysis: It's got a knack for sorting through financial reports to give you the gist of what's going on.
* Market Tracking: Keeps an eye on your favorite companies and nudges you at the right moments, like when to buy or sell.
* Timely Reminders: Ensures you don't miss out on important company updates, especially when the execs are making moves.

### The Tech Stuff
* TradeWiSE is built as a series of microservices, using Python, FastAPI, and Docker.
* It's currently set up with Telegram for interaction, but it’s designed to be adaptable to other messaging platforms.

### Jump In, Let's Collaborate:
* If stocks or coding are your things, or if you're just curious, feel free to hop in. There's room for ideas and improvements!
* We're rolling with the Mozilla license, keeping it open for everyone to contribute.
* Peek at the DEVELOPER_GUIDE for the nitty-gritty on how TradeWiSE works.

## Installation Guide

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

## License
This project, TradeWiSE, is primarily licensed under the Mozilla Public License 2.0 (MPL 2.0). This license grants freedoms for the use, modification, and sharing of the code while requiring that any modifications be distributed under the same license.

### Main Project License
All code in this project, except for the service specifically mentioned below, is released under the Mozilla Public License 2.0. You can find the complete license agreement for the majority of the project in the root directory of this project.

### Special Service License - data-analysis
The data-analysis service within this project is licensed under the MIT License. This is a more permissive license that allows users to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the service with minimal restrictions.

The specific terms of the MIT License for the data-analysis service can be found in the LICENSE file within its directory.

The rationale behind using different licenses in this project is to accommodate varying degrees of openness and reuse within its components. The MPL 2.0 license, used for the majority of the project, ensures that modifications to the code remain open. However, for the data-analysis service, which involves strategies and methods that individuals might want to modify more freely, the MIT license offers the necessary flexibility. This allows contributors and users of the data-analysis service to adapt and use the code with fewer restrictions, fostering innovation and broader use in diverse contexts.

### Note to Contributors

All contributions to the TradeWiSE project, regardless of size, are considered to be released under the Mozilla Public License 2.0, unless specified otherwise. Contributions to the data-analysis service should adhere to the MIT License.