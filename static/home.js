$(document).ready(function(){

    $('#search_input').focus()
    console.log

    data.forEach(elem => add_link(elem))

    function add_link(elem){
        let id = elem.id
        let jq = '#card'+id
        let url= window.location.search +'/view/'+id
        $(jq).attr("href", url)
    }

}) //document.ready

