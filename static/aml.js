import * as con from './daemon_connection.js'

export {aml}


class aml {
    constructor(url, elementPrefix) {
        this.url = url;
        this.elementPrefix = elementPrefix;
        this.connectionId = elementPrefix + '_connect_status';
        this.errorId = elementPrefix + '_error_status';
        this.busyId = elementPrefix + '_busy_status';
        this.requestId = elementPrefix + '_request_id';
        this.firstMotorId = elementPrefix + '_first';
        this.secondMotorId = elementPrefix + '_second';
        this.requestStatus = elementPrefix + '_request_status';

        this.firstMotorRequest = elementPrefix + '_first_request';
        this.secondMotorRequest = elementPrefix + '_second_request';
    }

    async init() {
        await this.updateActuals();
    }

    async updateActuals(){
        return fetch(this.url + '/actuals')
            .then(response => {
                con.setConnected(this.connectionId, true);
                return response.json();
            })
            .then(data => {
                con.getEl(this.firstMotorId).innerText =
                    data['motor1']['position_real_world'];
                con.getEl(this.secondMotorId).innerText =
                    data['motor2']['position_real_world'];
                con.getEl(this.requestId).innerText = data['request_id'];

                if (data['error_status'] !== 'Success') {
                    con.collapsableError(this.errorId, data['error_status']);
                } else {
                    con.getEl(this.errorId).innerHTML = '';
                }
                updateSpinnerVisbility(this.busyId, data);
                return data;
            })
            .catch(error => {
                con.setConnected(this.connectionId, false);
                con.collapsableError(this.errorId, error);
                con.getEl(this.firstMotorId).innerText = '-';
                con.getEl(this.secondMotorId).innerText = '-';
                con.getEl(this.requestId).innerText = '-';
            });
    }

    async sendRequest(request) {
        let requestId = con.getUniqueIdentifier();
        let fullRequest = 'request_id=' + requestId + '\n';
        fullRequest += request;
        con.postData(this.url + '/engine', fullRequest);
        let expiry_date = await this.getCompletionTime(requestId, 10, 0);
        if (expiry_date !== undefined) {
            con.collapsableSucess( this.requestStatus,
                'Request sent with id: ' + requestId +
                ', should be done at: ' + expiry_date);
        }
    }

    async getCompletionTime(requestId, retryLimit, retryCount) {
        return this.updateActuals().then(data => {
            if (data['request_id'] === requestId) {
                return data['expiry_date'];
            } else if (retryCount < retryLimit) {
                return con.delay(100)
                    .then(() => this.getCompletionTime(requestId, retryLimit, retryCount + 1));
            }
        });
    }

    submitMotors() {
        let first_pos = con.getEl(this.firstMotorRequest).value;
        let second_pos = con.getEl(this.secondMotorRequest).value;

        let request = '';
        if (first_pos && second_pos) {
            request += 'set_m1_target_position=' + first_pos + '\n';
            request += 'set_m2_target_position=' + second_pos + '\n';
            this.sendRequest(request);
        } else if (first_pos) {
            request += 'set_m1_target_position=' + first_pos + '\n';
            this.sendRequest(request);
        } else if (second_pos) {
            request += 'set_m2_target_position=' + second_pos + '\n';
            this.sendRequest(request);
        } else {
            con.collapsableError(this.requestStatus, 'No input provided');
        }
    }

    loadMotors() {
        con.getEl(this.firstMotorRequest).value = '60';
        con.getEl(this.secondMotorRequest).value = '10';
        this.submitMotors();
    }

    unLoadMotors() {
        con.getEl(this.firstMotorRequest).value = '0';
        con.getEl(this.secondMotorRequest).value = '0';
        this.submitMotors();
    }

    continueOnError() {
        this.sendRequest('continue=true');
    }
}

function updateSpinnerVisbility(elementId, data) {
    if (data['status'] === 'Processing') {
        con.getEl(elementId).style.display = 'block';
    } else if (data['status'] === 'Done') {
        con.getEl(elementId).style.display = 'none';
    }
}
