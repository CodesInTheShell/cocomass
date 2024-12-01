export const listAssessments = () => {
    return axios.get('/assessments')
        .then((response) => {
            return response
        }).catch((e) => {
            return ''
    })
}

export const searchAssessments = (query) => {
    return axios.get(`/assessments?query=${query}`)
        .then((response) => {
            return response
        }).catch((e) => {
            return ''
    })
}

export const deleteAssessmentById = (id) => {
    return axios.delete('/assessments/'+id)
        .then((response) => {
            return response
        }).catch((e) => {
            return ''
    })
}