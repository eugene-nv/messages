new Vue(
    {
        el: "#list_app",
        data: {
            messages: []
        },
        created: function () {
            const vm = this;
            axios.get('/api/message/')
            .then(function (response){
                vm.messages = response.data
            })
        }
    },
)