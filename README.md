**Splunk → Confluence Alert Action 🚀**

Publish Splunk alert results **directly** into Atlassian Confluence pages.\
No more screenshots, no more manual copy-paste: **your dashboards update themselves**.

* * * * *

**✨ Why it's cool**

-   **Direct integration** → from Splunk alerts straight into Confluence.

-   **Zero manual effort** → once installed, pages stay fresh and aligned with your data.

-   **GUI configurable** → all parameters are entered in Splunk's alert action form, no code changes.

-   **Confluence-ready HTML** → clean tables, alternating row colors, blue headers, auto timestamp.

-   **Zero dependencies** → pure Python (`urllib` only), works on Splunk Enterprise and Splunk Cloud.

-   **Customizable template** → edit a simple HTML file to change the look and feel.

* * * * *

**⚡ Installation**

1.  Download the latest `.tgz` package from Releases.

2.  In Splunk Web: **Apps → Manage Apps → Install app from file**.

3.  Upload the package and restart Splunk.\
    Done. Your Splunk just learned how to talk to Confluence.

* * * * *

**⚙️ How it works**

1.  Create or edit an alert in Splunk.

2.  In **Trigger Actions**, select **Send to Confluence**.

3.  Fill in your Confluence details:

    -   **Base URL** (example: `https://yourcompany.atlassian.net/wiki`)

    -   **Page ID**

    -   **Space Key**

    -   **Page Title**

    -   **User** and **API Token**

4.  Save and let it run.

When the alert fires, your Confluence page is updated instantly with the results.

* * * * *

**📄 Example Output**

-   Blue Confluence-style header

-   Clean data table with alternating rows

-   Automatic timestamp of last update

-   Info macro with alert context

(*Insert screenshot here for maximum wow-effect*)

* * * * *

**🗂 Repository Layout**

-   `bin/splunk_to_confluence.py` → main script

-   `default/alert_actions.conf` → action definition

-   `README/alert_actions.conf.spec` → GUI parameters

-   `metadata/default.meta` → system export

-   `templates/confluence_template.html` → customizable HTML template

-   `README.md` → this file

* * * * *

**🚀 Example savedsearch**

`[Send Docker Services to Confluence]
action.splunk_to_confluence = 1
action.splunk_to_confluence.BASE_URL = https://yourcompany.atlassian.net/wiki
action.splunk_to_confluence.PAGE_ID = 123456789
action.splunk_to_confluence.SPACE_KEY = OPS
action.splunk_to_confluence.PAGE_TITLE = Docker Services Snapshot
action.splunk_to_confluence.AUTH_USER = bot@yourcompany.com
action.splunk_to_confluence.AUTH_TOKEN = <api-token>
cron_schedule = */90 * * * *
search = index="docker_system-logs" sourcetype=json_no_timestamp ...`

* * * * *

**📜 License**\
MIT License -- free to use, share and improve.

* * * * *

**🤝 Contributing**\
Pull requests are welcome!\
You can:

-   Improve the HTML styling

-   Add richer statistics

-   Extend with attachments or macros

* * * * *

**🙌 Why it matters**\
Because nobody should waste time taking screenshots of Splunk dashboards.\
With this TA, your Confluence pages are **always live, always fresh, always automated**.

**CREDITS**\
Marco Gomiero (programming)
Riccardo Natale (quality assurance and testing)