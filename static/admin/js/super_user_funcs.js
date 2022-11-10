function get_permissions_list(permissions_list_url, permission_list=[]) {
    $.ajax({
        type: 'GET',
        url: permissions_list_url,
        success: function (response) {
            $('#permissions_div').show();
            $('#permissions').append(
                '<option disabled value="" >Please select</option>'
            );
            $.map(response, function (data) {
                let isSelected = false;
                if(permission_list.length && permission_list.includes(data.id)){
                    isSelected = true;
                    console.log(isSelected, permission_list, data.id)
                }
                $('#permissions').append(
                    `<option 
                        value="${data.id}"
                        ${isSelected? 'selected' : ''}
                    >
                        ${data.name}
                    </option>`
                )
            })
        },
        error: function (xhr, msg, err) {
            alert(xhr.responseJSON.error);
        }
    });
}