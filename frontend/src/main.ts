import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@/assets/css/tailwind.css';

import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';

import Drawer from 'primevue/drawer';
import Button from 'primevue/button';
import Menubar from 'primevue/menubar';
import DataTable from 'primevue/datatable';
import Column from "primevue/column";
import Chip from 'primevue/chip';
import MultiSelect from 'primevue/multiselect';
import Dialog from 'primevue/dialog';
import ProgressSpinner from 'primevue/progressspinner';
import Tooltip from 'primevue/tooltip';
import PanelMenu from 'primevue/panelmenu';
import Select from 'primevue/select';
import Divider from 'primevue/divider';
import Card from 'primevue/card';

import { createPinia } from 'pinia';

import 'primeicons/primeicons.css';

const pinia = createPinia();
const app = createApp(App);

app.component('Drawer', Drawer);
app.component('Button', Button);
app.component('Menubar', Menubar);
app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('Chip', Chip);
app.component('MultiSelect', MultiSelect);
app.component('Dialog', Dialog);
app.component('ProgressSpinner', ProgressSpinner);
app.component('PanelMenu', PanelMenu);
app.component('Select', Select);
app.component('Divider', Divider);
app.component('Card', Card);
  
app.directive('Tooltip', Tooltip);

app.use(pinia);
app.use(PrimeVue, {
  theme: { preset: Aura }
});
app.use(router);

app.mount('#app');