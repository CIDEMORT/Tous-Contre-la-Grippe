import APIHandler from '../APIHandler';
const resource = 'geographie';

export default {
    getEvolutionActesRegion() {
        return APIHandler.get(`${resource}/evolution-actes-region`);
    }
}