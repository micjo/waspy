import * as con from './daemon_connection.js'

export {
    aml
}


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
        this.firstMotorTemperature = '-';
        this.firstMotorStepCounter = '-';
        this.firstMotorOffset = '-';
        this.secondMotorTemperature = '-';
        this.secondMotorStepCounter = '-';
        this.secondMotorOffset = '-';

        this.gettingFirstPos = false;
        this.gettingFirstTemp = false;
        this.gettingSecondPos = false;
        this.gettingSecondTemp = false;
    }

    removeData() {
        this.error = '-';
        this.busy = '-';
        this.requestId = '-';
        this.firstMotorPosition = '-';
        this.secondMotorPosition = '-';
        this.requestAcknowledge = true;
        this.completionTIme = '-';
        this.firstMotorTemperature = '-';
        this.firstMotorStepCounter = '-';
        this.firstMotorOffset = '-';
        this.secondMotorTemperature = '-';
        this.secondMotorStepCounter = '-';
        this.secondMotorOffset = '-';
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
            .catch( () => {
                this.connected = false;
            })
            .then(data => {
                this.requestId = data['request_id'];
                this.firstMotorPosition = data['motor1']['position_real_world'];
                if (data['motor1']['temperature']) {
                    this.firstMotorTemperature = data['motor1']['temperature'];
                }
                else {
                    this.firstMotorTemperature = '-';
                }
                this.firstMotorStepCounter = data['motor1']['position_steps'];
                this.firstMotorOffset = data['motor1']['offset'];
                this.secondMotorPosition = data['motor2']['position_real_world'];
                if (data['motor2']['temperature']) {
                    this.secondMotorTemperature = data['motor2']['temperature'];
                }
                else {
                    this.secondMotorTemperature = '-';
                }
                this.secondMotorStepCounter = data['motor2']['position_steps'];
                this.secondMotorOffset = data['motor2']['offset'];
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

    async getFirstPosition() {
        let request = 'current_m1_position=true\n';
        await this.sendRequest(request);
    }

    async getFirstTemperature() {
        let request = 'get_m1_current_temperature=true\n';
        await this.sendRequest(request);
    }

    async redefineFirstStepCounter(newValue) {
        let request = 'set_m1_step_counter=' + newValue + '\n';
        await this.sendRequest(request);
    }

    async redefineFirstPosition(newValue) {
        let request = 'redefine_m1_position=' + newValue + '\n';
        await this.sendRequest(request);
    }

    async redefineFirstOffset(newValue) {
        let request = 'set_m1_offset=' + newValue + '\n';
        await this.sendRequest(request);
    }

    async toggleFirstPositionUpdate() {
        this.gettingFirstPos = !this.gettingFirstPos;
        let request = 'get_idle_update_m1_position='
        if (this.gettingFirstPos) {
            request += 'true\n';
        }
        else {
            request += 'false\n';
        }
        await this.sendRequest(request);
    }

    async toggleFirstTemperatureUpdate() {
        this.gettingFirstTemp = !this.gettingFirstTemp;
        let request = 'get_idle_update_m1_temperature='
        if (this.gettingFirstTemp) {
            request += 'true\n';
        }
        else {
            request += 'false\n';
        }
        await this.sendRequest(request);
    }

    async getSecondPosition() {
        let request = 'current_m2_position=true\n';
        await this.sendRequest(request);
    }

    async getSecondTemperature() {
        let request = 'get_m2_current_temperature=true\n';
        await this.sendRequest(request);
    }

    async redefineSecondStepCounter(newValue) {
        let request = 'set_m2_step_counter=' + newValue + '\n';
        await this.sendRequest(request);
    }

    async redefineSecondPosition(newValue) {
        let request = 'redefine_m2_position=' + newValue + '\n';
        await this.sendRequest(request);
    }

    async redefineSecondOffset(newValue) {
        let request = 'set_m2_offset=' + newValue + '\n';
        await this.sendRequest(request);
    }

    async toggleSecondPositionUpdate() {
        this.gettingSecondPos = !this.gettingSecondPos;
        let request = 'get_idle_update_m2_position='
        if (this.gettingSecondPos) {
            request += 'true\n';
        }
        else {
            request += 'false\n';
        }
        await this.sendRequest(request);
    }

    async toggleSecondTemperatureUpdate() {
        this.gettingSecondTemp = !this.gettingSecondTemp;
        let request = 'get_idle_update_m2_temperature='
        if (this.gettingSecondTemp) {
            request += 'true\n';
        }
        else {
            request += 'false\n';
        }
        await this.sendRequest(request);
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
