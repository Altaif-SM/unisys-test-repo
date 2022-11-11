function getCityData(getCityDataUrl){
    const CityOptions = $("#id_city")

    $.ajax({
        type: 'GET',
        url: getCityDataUrl,
        data: {
            "type": "JSON",
            "country": $("#id_country").val(),
        },
        success: function (response) {
            const jsonRes = JSON.parse(response)

            CityOptions.empty()
            CityOptions.prepend($('<option>',{
                value: '',
                text: "Select City",
                "selected": true,
            }))
            $.map(jsonRes, function(data){
                CityOptions.append($('<option>', {
                    value: data.pk,
                    text : data.fields.city
                }));
            })
        },
        complete: function (){
        },
        error: function (xhr, msg, err) {
        }
    });
}