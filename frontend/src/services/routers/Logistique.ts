import APIHandler from '../APIHandler';
const resource = 'logistique';

export default {
    getActesDosesRegion() {
        return APIHandler.get(`${resource}/actes-doses-region`);
    }
}