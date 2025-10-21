import APIHandler from '../APIHandler';
const resource = 'saisonnalite';

export default {
    getDonneesMeteo() {
        return APIHandler.get(`${resource}/donnees-meteo`);
    }
}