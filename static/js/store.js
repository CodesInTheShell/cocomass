function newVueStore() {
    return {
        testStoreText: "AI pre-commit code reviewer and assistant",
    }
}

const store = {
    
    state: Vue.reactive(newVueStore()), 

    gettestStoreText() {
        return this.state.testStoreText
    },
}
export default store