<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>My Vocabulary</title>
    <meta property="og:title" content="Vocabs"/>
    <meta property="og:description" content="Find, Save and Manage Your Vocabs!"/>
    <meta property="og:image" content="{{ url_for('static', filename='logo_red.png') }}"/>
    <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
          crossorigin="anonymous">
    <link href='{{ url_for("static", filename="mystyle.css") }}' rel="stylesheet">
    <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
            integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
            crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
            integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
            crossorigin="anonymous"></script>
    <style>
        .search-box {
            width: 70%;
            margin: 50px auto;
            max-width: 700px;
        }

        .table {
            width: 80%;
            max-width: 800px;
            margin: auto;
            table-layout: fixed;
        }

        .table th {
            border-top-style: none;
        }

        td {
            background-color: white;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
        }

        td > a, a:visited, a:hover, a:active {
            color: black;
        }

        tr.highlight > td {
            background-color: #a1a1a1;
            color: white    ;
        }

        tr.highlight a {
            color: white;
        }

        thead:first-child tr:first-child th:first-child {
            border-radius: 10px 0 0 0;
        }

        thead:first-child tr:first-child th:last-child {
            border-radius: 0 10px 0 0;
        }

        tbody:last-child tr:last-child td:first-child {
            border-radius: 0 0 0 10px;
        }

        tbody:last-child tr:last-child td:last-child {
            border-radius: 0 0 10px 0;
        }
    </style>
    <script>
        {% if pyAlert %}
            alert("{{ alert }}")
        {% endif %}

        let wordLists = {{ pyWords|tojson}}
            console.log(wordLists)
        let word_list = []
        for (let i = 0; i < wordLists.length; i++) {
            word_list.push(wordLists[i]["word"])
        }
        console.log(word_list)

        function find_word() {
            let insert_word = $("#search-word").val().toLowerCase()
            console.log(insert_word)
            if (word_list.includes(insert_word)) {
                console.log("word was saved")
                $(`#word-${insert_word}`).addClass("highlight")
                $(`#word-${insert_word}`).siblings().removeClass("highlight")
                $(`#word-${insert_word}`).get(0).scrollIntoView()
            } else {
                window.location.href=`/detail/${insert_word}?condition_give=new`
            }
        }
    </script>
</head>
<body>
<div class="wrap">
    <div class="banner" onclick="window.location.href = '/'">
    </div>
    <div class="search-box d-flex justify-content-center">
        <input id="search-word" class="form-control" style="margin-right: 0.5rem">
        <button class="btn btn-light" onclick="find_word()"><i class="fa fa-search"></i></button>
    </div>

    <table class="table">
        <thead class="thead-light">
        <tr>
            <th scope="col" style="width:30%">WORD</th>
            <th scope="col">MEANING</th>

        </tr>
        </thead>
        <tbody id="tbody-box">
        {% for saved_word in pyWords %}
        <tr id="word-{{ saved_word.word }}">
            <td><a href="/detail/{{ saved_word.word }}?condition_give=old">{{ saved_word.word }}</a></td>
            <td>{{ saved_word.defin|safe}}
            </td>
        </tr>
        {% endfor %}
        </tbody>
    </table>

</div>


</body>
</html>
