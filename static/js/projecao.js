const socket = io();


/* =====================================
   RECEBER TEXTO
===================================== */

socket.on(
    "atualizar_projecao",
    function (dados) {

        const texto =
            document.getElementById("texto");

        const tela =
            document.getElementById("tela");


        texto.innerText =
            dados.texto;


        texto.style.fontSize =
            dados.tamanho + "px";


        texto.style.color =
            dados.corTexto;


        tela.style.background =
            dados.corFundo;

    }
);


/* =====================================
   LIMPAR
===================================== */

socket.on(
    "limpar_projecao",
    function () {

        document.getElementById(
            "texto"
        ).innerText = "";

    }
);


/* =====================================
   DUPLO CLIQUE = TELA CHEIA
===================================== */

document.addEventListener(
    "dblclick",
    function () {

        document.documentElement
            .requestFullscreen()
            .catch(() => {});

    }
);


/* =====================================
   ESC
===================================== */

document.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Escape" &&
            document.fullscreenElement
        ) {

            document.exitFullscreen();

        }

    }
);