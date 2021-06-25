const csrftoken = Cookies.get('csrftoken');
var table_data = []
var num_items = 0
var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "data", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
    xhttp.onload = function () {
    if (xhttp.readyState = XMLHttpRequest.DONE){
        var db_json = JSON.parse(xhttp.responseText);
        db_json.racks = JSON.parse(db_json.racks);
           for(i=0; i < Object.keys(db_json.racks).length;i++) {
               db_row = db_json.racks[i];
               table_data[i] = [db_row.fields.part_number, db_row.fields.description, db_row.fields.location, db_row.fields.ip, db_row.pk];
           };
           load_table();
};
};
function load_table(racks_json){
    $(document).ready(function(){
        table = $('#racks_table').DataTable({
            select: 'row',
            multiselect: true,
            data: table_data,
            order: [[4, 'asc']],
            paging: false,
            columns: [
            { title: "Part Number" },
            { title: "Description" },
            { title: "Location" },
            { title: "IP" },
            { title: "ID" }]
        });

        checkout_table = $('#checkout_table').DataTable({
            select: 'row',
            multiselect: true,
            data: [[' ',' ',' ', ' ', ' ']],
            order: [1, 'asc'],
            paging: false,
            dom: 'Bfrtip',
            buttons: [{
            text: 'Find Items',
            action: function ( e, dt, node, config ) {
                checkout();
            }}],
            columns: [
            { title: "Part Number" },
            { title: "Description" }],
        });
        checkout_table.clear();


        table.on('select', function(e, dt, type, indexes){
            if(type === 'row'){
                rows= table.rows('.selected').data();
                for(i=0; i < rows.length; i++){
                    if((rows[i][4] - 1) == indexes[0]){
                    selected_row = [rows[i][0], rows[i][1], rows[i][2], rows[i][3], rows[i][4]];
                }};
                checkout_table.row.add(selected_row).draw();
        }});
        table.on('deselect', function(e, dt, type, indexes){
                if(type === 'row'){
                row_index = parseInt(table.rows(indexes)[0]) + 1;
                for(I=0; I < checkout_table.rows().data().length;I++){
                    checkout_row = checkout_table.row(I).data()[4];
                    if(row_index == checkout_row){
                        checkout_table.row(I).remove().draw();
                        break;
                }};
        }});

        checkout_table.on('select', function(e, dt, type, indexes){
        //TODO Indexing is very broken here
            if(type === 'row'){
                row_to_deselect_index = checkout_table.rows(indexes).data()[0][4];
                console.log(row_to_deselect_index, indexes)
                checkout_table.row(checkout_table.rows(indexes)[0]).remove().draw();

                table.row(row_to_deselect_index  - 1).deselect();

        }});
    });
};
function checkout(){
    part_dictionary = [];
    for(i=0; i < checkout_table.rows().data().length;i++){
        part_dictionary[i] = checkout_table.rows().data()[i];
    };

        $.ajaxSetup({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }});

    $.ajax({
        type: "POST",
        data: {'parts':JSON.stringify(part_dictionary)},
        dataType: "json",
        url: "map"
    }).done(function (res) {
    console.log(res)
    });
    window.location.href = 'map';

};
