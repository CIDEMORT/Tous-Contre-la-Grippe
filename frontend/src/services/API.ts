import RolesAPI from "@/services/routers/RolesAPI";
import GeographieAPI from "@/services/routers/GeographieAPI";
import Saisonnalite from "./routers/Saisonnalite";
import Logistique from "./routers/Logistique";

export default {
    roles: RolesAPI,
    geographie: GeographieAPI,
    saisonnalite: Saisonnalite,
    logistique: Logistique
}