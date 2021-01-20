import * as con from './daemon_connection.js'

export {caen}

class caen {
    constructor(url) {
        this.url = url;
        this.connected = false;
        this.error = '-';
        this.requestId = '-';
        this.acquiringData = '-';
        this.histogramLocation = '-';
        this.listDataLocation = '-';
        this.listDataTimeout = '-';
        this.listDataStoring = '-';
        this.listDataSaving = false;
        this.acquiringData = false;
        this.requestAcknowledge = true;
    }

    removeData() {
        this.requestId = '-';
        this.acquiringData = '-';
        this.histogramLocation = '-';
        this.listDataLocation = '-';
        this.listDataTimeout = '-';
        this.listDataSaving = false;
        this.acquiringData = false;
        this.requestAcknowledge = true;
    }

    async init() {
        await this.updateActuals();
    }

    async updateActuals() {
        return fetch(this.url + '/actuals')
            .then(response => {
                this.connected = true;
                return response.json();
            })
            .catch(() => {
                this.connected = false;
            })
            .then(data => {
                this.requestId = data['request_id'];
                this.acquiringData = data['acquiring_data'];
                this.histogramLocation = data['histogram']['location'];
                this.listDataSaving = data['list_data']['storing'];
                this.listDataLocation= data['list_data']['location'];
                this.listDataTimeout = data['list_data']['timeout_minutes'];
                this.error = data['error_status'];
            })
            .catch(() => {
                this.error = "Problem when parsing data";
                this.removeData();
            });
    }

    async waitForCompleted(requestId, retryLimit, retryCount) {
        return this.updateActuals().then( () => {
            if (this.requestId === requestId) {
                this.requestAcknowledge = true;
                return;
            }
            else if (retryCount < retryLimit) {
                console.log('wait for complete');
                return con.delay(100)
                    .then( () => this.waitForCompleted(requestId, retryLimit, retryCount + 1));
            }
            else {
                this.requestAcknowledge = false;
            }
        })
    }

    async saveHistogram(histogramFolder) {
        let request = "store_histogram=true\n";
        request += "store_histogram_folder=" + histogramFolder; + "\n";
        await this.sendRequest(request);
    }

    async sendRequest(request) {
        this.requestAcknowledge = true;
        let requestId = con.getUniqueIdentifier();
        let fullRequest = 'request_id=' + requestId + '\n';
        fullRequest += request;
        await con.postData(this.url + '/engine', fullRequest);
        await this.waitForCompleted(requestId, 30, 0);
    }

    async toggleAcquire() {
        let acquireTry = this.acquiringData;
        acquireTry = !acquireTry;
        if (acquireTry) {
            await this.sendRequest("start_acquisition=true");
        }
        else {
            await this.sendRequest("stop_acquisition=true");
        }
    }

    async startStoringListData(listDataFolder, timeout) {
        let request = "store_list_data=true\n";
        request += "store_list_data_folder=" + listDataFolder + "\n";
        request += "store_list_data_timeout_minutes=" + timeout + "\n";
        await this.sendRequest(request);
    }

    async getHistogram(boardNr, channelNr) {
        return fetch(this.url + "/histogram/" + boardNr + "-" + channelNr)
            .then(response => {return response.text();})
            .catch(error => console.log(error));
    }

    async stopStoringListData() {
        let request = "store_list_data=false\n";
        await this.sendRequest(request);
    }

    async continueOnError() {
        await this.sendRequest('continue=true');
    }

    async clearData() {
        await this.sendRequest('clear_acquisition=true');
    }

    async saveRegistry() {
        await this.sendRequest('store_registry=true');
    }
}
