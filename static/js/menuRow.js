
currPage = 1;
search = ""
currentOrder = "id"


window.addEventListener('DOMContentLoaded', (event) => {
    currentOrder = "id"
    getCardsReplace2("", 1);
});


function changeOrder2(str) {
    element = document.getElementById(str)
    dataValue = element.getAttribute("data-value");
    if (dataValue.startsWith("-")) {
        element.setAttribute("data-value", dataValue.replace("-", ""))
        dataValue = dataValue.replace("-", "")
        document.getElementById(str + "Chevron").setAttribute("d", "M19.5 8.25l-7.5 7.5-7.5-7.5")
    }
    else {
        element.setAttribute("data-value", "-" + dataValue)
        dataValue = "-" + dataValue
        document.getElementById(str + "Chevron").setAttribute("d", "M4.5 15.75l7.5-7.5 7.5 7.5")

    }
    currPage = 1;
    currentOrder = dataValue
    getCardsReplace2(search, currPage)

}




function getCardsReplace2(search, page = 1, element) {
    if (element && element.id) {
        var searchBarFId = element.id;

        var match = searchBarFId.match(/(\d+)$/);
        var number = match ? parseInt(match[1], 10) : null;


        var targetId = "searchBarMenu_" + number;
        console.log(targetId);

        search = search;
        currPage = 1;

        fetch('AjaxSearch2', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'jsonBody': { "search": search, "page": page, "orderBy": currentOrder } })
        })
            .then(response => response.text())
            .then(text => {
                console.log(text);
                var cardHolderId = 'cardHolder2_' + number;
                var elementosLista = [];

                // Crear un elemento temporal (div)
                var tempDiv = document.createElement('div');

                // Asignar el HTML al 'innerHTML' del elemento temporal
                tempDiv.innerHTML = text;

                // Obtener el elemento 'cardHolder2_'
                var cardHolder = document.getElementById(cardHolderId);

                // Limpiar el contenido actual de 'cardHolder2_'
                cardHolder.innerHTML = '';

                // Iterar sobre los elementos hijos del elemento temporal y agregarlos a 'cardHolder2_'
                for (var i = 0; i < tempDiv.children.length; i++) {
                    var child = tempDiv.children[i];

                    // Generar un ID dinámico basado en el número proporcionado
                    var nuevoId = child.id + number;

                    // Asignar el nuevo ID al elemento
                    child.id = nuevoId;

                    // Iterar sobre los elementos internos y actualizar sus IDs
                    child.querySelectorAll('[id]').forEach(function (element) {
                        element.id = element.id  + number;
                    });

                    cardHolder.appendChild(child);

                    // Puedes realizar operaciones adicionales aquí, si es necesario
                    // ...

                    // Agregar información a la lista
                    elementosLista.push({
                        'id': nuevoId,
                        'imagen': child.querySelector('img').src,
                        'texto': child.querySelector('span').textContent
                    });

                    // Imprimir el ID del elemento recién agregado
                    console.log('ID del elemento recién agregado:', nuevoId);
                }

                // Imprimir la lista de elementos
                console.log('Lista de elementos:', elementosLista);
            });





    }
  
     else {
     
        search = search
        console.log(search)
        currPage = 1;

        fetch('AjaxSearch2', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'jsonBody': { "search": search, "page": page, "orderBy": currentOrder } })
        })
            .then(response => response.text())
            .then(text => {
                console.log("Primera vez")
                document.getElementById('cardHolder2_').innerHTML = ``
                document.getElementById('cardHolder2_').innerHTML += text


            })
    }    


}




function getCardsPaged2(page = 1) {

    fetch('AjaxSearch2', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'jsonBody': { "search": search, "page": page, "orderBy": currentOrder } })
    })
        .then(response => response.text())
        .then(text => {
            document.getElementById('cardHolder2_1').innerHTML += text

        })
}

$(document).ready(function () {
    $('.dropdown').each(function (key, dropdown) {
        var $dropdown = $(dropdown);
        $dropdown.find('.dropdown-menu a').on('click', function () {
            $dropdown.find('button').text($(this).text()).append(' <span class="caret"></span>');
        });
    });
});