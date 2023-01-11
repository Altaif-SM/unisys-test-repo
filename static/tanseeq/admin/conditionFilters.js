function getUniversityData(getUniversitiesUrl){
    $.ajax({
        type: 'GET',
        url: getUniversitiesUrl,
        data: {
            "type": "JSON",
        },
        success: function (response) {
            const jsonRes = JSON.parse(response)

            const universityOptions = $("#id_university")
            $.map(jsonRes, function(data){
                universityOptions.append($('<option>', { 
                    value: data.pk,
                    text : data.fields.university_name
                }));
            })
        },
        complete: function (){
        },
        error: function (xhr, msg, err) {
        }
    });
}
function getSubjectData(getUniversitiesUrl){
    $.ajax({
        type: 'GET',
        url: getUniversitiesUrl,
        data: {
            "type": "JSON",
        },
        success: function (response) {
            const jsonRes = JSON.parse(response)

            const subjectOptions = $("#id_subject")
            $.map(jsonRes, function(data){
                subjectOptions.append($('<option>', {
                    value: data.pk,
                    text : data.fields.course_name
                }));
            })
        },
        complete: function (){
        },
        error: function (xhr, msg, err) {
        }
    });
}
function getFacultyData(getFacultyDataUrl){
    const facultyOptions = $("#id_faculty")

    $.ajax({
        type: 'GET',
        url: getFacultyDataUrl,
        data: {
            "type": "JSON",
            "university": $("#id_university").val(),
        },
        success: function (response) {
            const jsonRes = JSON.parse(response)

            facultyOptions.empty()
            facultyOptions.prepend($('<option>',{
                value: '',
                text: "Select Faculty",
                "selected": true,
            }))
            $.map(jsonRes, function(data){
                facultyOptions.append($('<option>', { 
                    value: data.pk,
                    text : data.fields.name 
                }));
            })
        },
        complete: function (){
        },
        error: function (xhr, msg, err) {
        }
    });
}

function getStudyModeData(getStudyModeDataUrl){
    const studyModeOptions = $("#id_study_mode")

    $.ajax({
        type: 'GET',
        url: getStudyModeDataUrl,
        data: {
            "type": "JSON",
            "university": $("#id_university").val(),
        },
        success: function (response) {
            const jsonRes = JSON.parse(response)

            studyModeOptions.empty()
            studyModeOptions.prepend($('<option>',{
                value: '',
                text: "Select Study Mode",
                "selected": true,
            }))
            $.map(jsonRes, function(data, index){
                studyModeOptions.append($('<option>', { 
                    value: data.pk,
                    text : data.fields.study_mode 
                }));
            })
        },
        complete: function (){
        },
        error: function (xhr, msg, err) {
        }
    });
}

function getProgramData(getProgramDataUrl){
    const programOptions = $("#id_program")

    $.ajax({
        type: 'GET',
        url: getProgramDataUrl,
        data: {
            "type": "JSON",
            "faculty": $("#id_faculty").val(),
            "university": $("#id_university").val(),
        },
        success: function (response) {
            const jsonRes = JSON.parse(response)

            programOptions.empty()
            programOptions.prepend($('<option>',{
                value: '',
                text: "Select Program",
                "selected": true,
            }))
            $.map(jsonRes, function(data){
                programOptions.append($('<option>', { 
                    value: data.pk,
                    text : data.fields.name
                }));
            })
        },
        complete: function (){
        },
        error: function (xhr, msg, err) {
        }
    });
}
