function newVueStore() {
    return {
        testStoreText: "A pre-commit code reviewer and assistant - AI code assessment tool",
    }
}

const store = {
    
    state: Vue.reactive(newVueStore()), 

    gettestStoreText() {
        return this.state.testStoreText
    },
}
export default store