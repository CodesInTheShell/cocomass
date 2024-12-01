import store from "./store.js";
import { deleteAssessmentById } from "./backend.js";

export default {
    props: ['assessments'],
    emits: ['refreshAssessments', 'searchquery'],
    data() {
        return {
            selectedComment: '', // To store the comment for modal display
            query: ''
        };
    },
    methods: {
        deleteAssessment(id) {
            // Implement your delete logic here, e.g., API call to remove the assessment
            console.log('Deleting assessment:', id);
            deleteAssessmentById(id)
            this.$emit('refreshAssessments')
        },
        toggleComment(id) {
            const selectedAssessment = this.assessments.find(a => a._id === id);
            this.selectedComment = selectedAssessment ? selectedAssessment.comment : 'No comment available.';
            
            // Trigger the modal programmatically using Bootstrap's API
            const modalElement = this.$refs.commentModal;
            if (modalElement) {
                const modal = new bootstrap.Modal(modalElement);
                modal.show();
            }
        },
        toMarkDown(){
            return marked.parse(this.selectedComment)
        },
    },
    computed: {
        hasAssessments() {
            return Array.isArray(this.assessments) && this.assessments.length > 0;
        }
    },
    template: /*html*/ `
        <div class="container mt-4">
            <h2 class="text-center mb-4">Code Commit Reviews</h2>
            <template v-if="hasAssessments">

                <div class="input-group input-group-sm mb-3">
                    <span class="input-group-text" id="inputGroup-sizing-sm">Search by commit hash</span>
                    <input v-model="query" type="text" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm">
                    <button type="button" class="btn btn-dark" @click="$emit('searchquery', query)">Search</button>
                </div>

                <div class="table-responsive">
                    <table class="table table-bordered table-striped table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th scope="col">Filename and Criticality</th>
                                <th scope="col">Commit Message</th>
                                <th scope="col">Commit Hash</th>
                                <th scope="col">Created At</th>
                                <th scope="col">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="assessment in assessments" :key="assessment._id">
                                <td>
                                    {{ assessment.filename || 'N/A' }}
                                    <p class="m-2">
                                        <span 
                                            class="badge bg-secondary"
                                            :class="{
                                                'bg-success': assessment.criticality === 'minor',
                                                'bg-info': assessment.criticality === 'moderate',
                                                'bg-warning': assessment.criticality === 'major',
                                                'bg-danger text-light': assessment.criticality === 'critical',
                                                'bg-secondary': !assessment.criticality
                                            }"
                                        >
                                            {{assessment.criticality || 'N/A'}}
                                        </span>
                                    </p>
                                </td>
                                <td>{{ assessment.commit_message || 'No commit message' }}</td>
                                <td>{{ assessment.commit_hash || 'N/A' }}</td>
                                <td>{{ assessment.created_at || 'N/A' }}</td>
                                <td>
                                    <button class="btn btn-danger btn-sm m-2" @click="deleteAssessment(assessment._id)">Delete</button>
                                    <button class="btn btn-info btn-sm ms-2" @click="toggleComment(assessment._id)">
                                        Show Comment
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </template>
            <template v-else>
                <p class="text-center text-muted">No assessments available.</p>
            </template>

            <!-- Modal for showing the comment -->
            <div class="modal fade" ref="commentModal" tabindex="-1" aria-labelledby="commentModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="commentModalLabel">Assessment Comment</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div v-html="toMarkDown()"></div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
};
