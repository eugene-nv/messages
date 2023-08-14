new Vue(
    {
        el: "#create_app",
        data: {
            message: {
                text: ''
              }
        },
        methods: {
            addForm() {
                axios
                  .post('/api/message/', this.messages
                  )
                  .catch(error => {
                    console.log('error', error)
                  })
            },
    }
}

)