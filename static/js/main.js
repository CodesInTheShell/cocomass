import store from './store.js';
import { listAssessments, searchAssessments } from "./backend.js"
import childComp from './childComp.js';

const app = Vue.createApp({
    data(){
        return {
            message: 'Welcome to Cocomass',
            storeText: store.gettestStoreText(),
            assessments: [],
        }
    },
    methods: {
        searchQuery(query){
            searchAssessments(query).then(function (response) {
                var res = response.data
                if (res != ''){
                    this.assessments = res
                } else {
                    console.error('Might have an error')
                }
            }.bind(this))
        },
        refreshAssessments(){
            listAssessments().then(function (response) {
                var res = response.data
                if (res != ''){
                    this.assessments = res
                } else {
                    console.error('Might have an error')
                }
            }.bind(this))
        }
    },
    created () {
        this.refreshAssessments()
        // listAssessments().then(function (response) {
        //     var res = response.data
        //     if (res != ''){
        //         this.assessments = res
        //     } else {
        //         console.error('Might have an error')
        //     }
        // }.bind(this))
    },
    components: {
        'child-comp': childComp,
    },
    template: /*html*/`
    <div class="container py-4">
        <div class="mt-4">
            <h1>{{message}}</h1>
            <h5>{{storeText}}</h5>
        </div>
        <hr>
        <child-comp
            :assessments='assessments'
            @refreshAssessments='refreshAssessments'
            @searchquery='searchQuery'
        >
        </child-comp>
    </div>
    `
})
app.use().mount('#app')