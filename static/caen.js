import * as con from './daemon_connection.js'

export {caen}

class caen {
    constructor(url, elementPrefix) {
        this.url = url;
        this.elementPrefix = elementPrefix;
        this.connectionEl = this.elementPrefix + '_connect_status';
        this.errorEl = this.elementPrefix + '_error_status';
        this.requestEl = this.elementPrefix + '_request_id';
        this.acquiringDataEl = this.elementPrefix + "_acquiring_data";
        this.acquiringDataButtonEl = this.elementPrefix + "_toggle_acquisition";
        this.listDataButtonEl = this.elementPrefix + "_toggle_list_data";
        this.requestStatus = this.elementPrefix + "_request_status";

        this.histogramNameEl = this.elementPrefix + "_histogram_id";
        this.histogramIdRequest = this.elementPrefix + "_histogram_id_request";

        this.listDataEl = this.elementPrefix + "_list_data_id";
        this.listDataIdRequest = this.elementPrefix + "_list_data_id_request";
        this.listDataTimeout = this.elementPrefix + "_list_data_timeout";
        this.listDataTimeoutRequest = this.elementPrefix + "_list_data_timeout_request";

        this.storingListData = this.elementPrefix + "_storing_list_data";

        this.acquiringText = "Acquisition started";
        this.notAcquiringText = "Acquisition stopped";
        this.savingListDataText = "Saving list data";
        this.notSavingListDataText = "Not saving list data";
    }

    async init() {
        await this.updateActuals();
    }

    async updateActuals() {
        return fetch(this.url + '/actuals')
            .then(response => {
                con.setConnected(this.connectionEl, true);
                return response.json();
            })
            .catch(() => {
                con.setConnected(this.connectionEl, false);
            })
            .then(data => {
                if (data === undefined) { throw("Cannot reach daemon"); }
                con.getEl(this.requestEl).innerText = data['request_id'];
                con.getEl(this.histogramNameEl).innerText = data['histogram']['location'];
                con.getEl(this.listDataEl).innerText = data['list_data']['location'];
                con.getEl(this.acquiringDataEl).innerText = data['acquiring_data'];
                con.getEl(this.storingListData).innerText = data['list_data']['storing'];

                this.acquiring = data['acquiring_data'];
                this.updateAcquireButton();

                this.savingListData = data['list_data']['storing'];
                this.updateListDataButton();

                con.getEl(this.listDataTimeout).innerText = data['list_data']['timeout_minutes'];

                if (data['error_status'] !== 'Success') {
                    con.collapsableError(this.errorEl, data['error_status']);
                } else {
                    con.getEl(this.errorEl).innerHTML = '';
                }
            })
            .catch(error => {
                con.collapsableError(this.errorEl, error);
                con.getEl(this.requestEl).innerText = '-';
                con.getEl(this.histogramNameEl).innerText = '-';
                con.getEl(this.listDataEl).innerText = '-';
                con.getEl(this.acquiringDataEl).innerText = '-';
            });
    }

    updateAcquireButton() {
        con.setButtonOnOrOff(this.acquiringDataButtonEl, this.acquiring, this.acquiringText, this.notAcquiringText);
    }

    updateListDataButton() {
        con.setButtonOnOrOff(this.listDataButtonEl, this.savingListData, this.savingListDataText, this.notSavingListDataText);
    }

    saveHistogram() {
        let id = con.getEl(this.histogramIdRequest).value;
        if(id) {
            let request = "store_histogram=true\n";
            request += "store_histogram_id=" + id; + "\n";
            this.sendRequest(request);
        }
        else {
            con.collapsableError(this.requestStatus, "To store histogram, " +
                "you need to specify to histogram id");
        }
    }

    async sendRequest(request) {
        let requestId = con.getUniqueIdentifier();
        let fullRequest = 'request_id=' + requestId + '\n';
        fullRequest += request;
        console.log(fullRequest);
        con.postData(this.url + '/engine', fullRequest);
    }

    toggleAcquisition() {
        this.acquiring = !this.acquiring;
        if (this.acquiring) {
            let request = "start_acquisition=true";
            this.sendRequest(request);
        }
        else {
            let request = "stop_acquisition=true";
            this.sendRequest(request);
        }
        this.updateAcquireButton();
    }

    toggleListData() {
        this.savingListData = !this.savingListData;
        if (this.savingListData) {
            let timeout = con.getEl(this.listDataTimeoutRequest).value;
            let id = con.getEl(this.listDataIdRequest).value;

            if (timeout && id) {
                let request = "store_list_data=true\n";
                request += "store_list_data_timeout_minutes=" + timeout + "\n";
                request += "store_list_data_id=" + id + "\n";
                this.sendRequest(request);
            }
            else {
                con.collapsableError(this.requestStatus, "To store list data, " +
                    "you need to specify timeout and id.");
            }
        }
        else {
            let request = "store_list_data=false\n";
            this.sendRequest(request);
        }
    }

    continueOnError() {
        this.sendRequest('continue=true');
    }
}
