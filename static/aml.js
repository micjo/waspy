import * as con from './daemon_connection.js'

export {aml}


class aml {
    constructor(url) {
        this.url = url;
        this.connected = false;
        this.error = '-';
        this.busy = '-';
        this.requestId = '-';
        this.firstMotorPosition = '-';
        this.secondMotorPosition = '-';
        this.requestAcknowledge = true;
        this.completionTime = '-';
    }

    removeData() {
        this.error = '-';
        this.busy = '-';
        this.requestId = '-';
        this.firstMotorPosition = '-';
        this.secondMotorPosition = '-';
        this.requestAcknowledge = true;
        this.completionTIme = '-';
    }

    async init() {
        await this.updateActuals();
    }

    async updateActuals(){
        return fetch(this.url + '/actuals')
            .then(response => {
                this.connected = true;
                return response.json();
            })
            .catch( () => {
                this.connected = false;
            })
            .then(data => {
                this.requestId = data['request_id'];
                this.firstMotorPosition = data['motor1']['position_real_world'];
                this.secondMotorPosition = data['motor2']['position_real_world'];
                this.error = data['error_status'];
                this.busy = data['status'];
                this.completionTime = data['expiry_date'];
            })
            .catch(() => {
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

    async sendRequest(request) {
        this.requestAcknowledge = true;
        let requestId = con.getUniqueIdentifier();
        let fullRequest = 'request_id=' + requestId + '\n';
        fullRequest += request;

        await con.postData(this.url + '/engine', fullRequest);
        await this.waitForCompleted(requestId, 30, 0);
    }

    async moveMotors(firstPosition, secondPosition) {
        let request ='';
        if (firstPosition && secondPosition) {
            request += 'set_m1_target_position=' + firstPosition + '\n';
            request += 'set_m2_target_position=' + secondPosition + '\n';
            await this.sendRequest(request);
        } else if (firstPosition) {
            request += 'set_m1_target_position=' + firstPosition + '\n';
            await this.sendRequest(request);
        } else if (secondPosition) {
            request += 'set_m2_target_position=' + secondPosition + '\n';
            await this.sendRequest(request);
        }
    }

    async continueOnError() {
        await this.sendRequest('continue=true');
    }
}
