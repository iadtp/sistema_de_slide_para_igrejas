const socket = io();


let apresentacaoAtual = null;

let slideAtual = null;


/* ======================================
   CONEXÃO
====================================== */

socket.on(
    "connect",
    function () {

        const status =
            document.getElementById(
                "status"
            );

        status.innerText =
            "● Conectado";

        status.style.color =
            "#00ff88";

        carregarApresentacoes();

    }
);


/* ======================================
   APRESENTAÇÕES
====================================== */

async function carregarApresentacoes() {

    const resposta =
        await fetch(
            "/api/apresentacoes"
        );


    const dados =
        await resposta.json();


    const lista =
        document.getElementById(
            "listaApresentacoes"
        );


    lista.innerHTML = "";


    dados.forEach(
        function (item) {

            const div =
                document.createElement(
                    "div"
                );


            div.className =
                "item-apresentacao";


            div.innerText =
                "📁 " + item.nome;


            div.onclick =
                function () {

                    selecionarApresentacao(
                        item.id,
                        item.nome
                    );

                };


            lista.appendChild(
                div
            );

        }
    );

}


/* ======================================
   NOVA APRESENTAÇÃO
====================================== */

async function novaApresentacao() {

    const nome =
        prompt(
            "Nome da apresentação:"
        );


    if (!nome) {

        return;

    }


    await fetch(
        "/api/apresentacoes",
        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"

            },

            body: JSON.stringify({

                nome: nome

            })

        }
    );


    carregarApresentacoes();

}


/* ======================================
   SELECIONAR
====================================== */

async function selecionarApresentacao(
    id,
    nome
) {

    apresentacaoAtual = id;

    slideAtual = null;


    document.querySelector(
        ".slides h2"
    ).innerText =
        "Slides — " + nome;


    await carregarSlides();

}


/* ======================================
   CARREGAR SLIDES
====================================== */

async function carregarSlides() {

    if (!apresentacaoAtual) {

        return;

    }


    const resposta =
        await fetch(

            `/api/apresentacoes/${apresentacaoAtual}/slides`

        );


    const slides =
        await resposta.json();


    const lista =
        document.getElementById(
            "listaSlides"
        );


    lista.innerHTML = "";


    slides.forEach(
        function (slide, index) {

            const div =
                document.createElement(
                    "div"
                );


            div.className =
                "item-slide";


            div.innerHTML = `

                <strong>
                    ${String(index + 1).padStart(2, "0")}
                </strong>

                <span>
                    ${slide.titulo || "Sem título"}
                </span>

            `;


            div.onclick =
                function () {

                    selecionarSlide(
                        slide
                    );

                };


            lista.appendChild(
                div
            );

        }
    );

}


/* ======================================
   NOVO SLIDE
====================================== */

async function novoSlide() {

    if (!apresentacaoAtual) {

        alert(
            "Selecione uma apresentação primeiro."
        );

        return;

    }


    const resposta =
        await fetch(

            `/api/apresentacoes/${apresentacaoAtual}/slides`,

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    titulo:
                        "Novo Slide",

                    texto:
                        ""

                })

            }

        );


    const dados =
        await resposta.json();


    await carregarSlides();


    slideAtual =
        dados.id;

}


/* ======================================
   SELECIONAR SLIDE
====================================== */

function selecionarSlide(slide) {

    slideAtual =
        slide.id;


    document.getElementById(
        "tituloSlide"
    ).value =
        slide.titulo || "";


    document.getElementById(
        "textoSlide"
    ).value =
        slide.texto || "";


    document.getElementById(
        "tamanho"
    ).value =
        slide.tamanho;


    document.getElementById(
        "corTexto"
    ).value =
        slide.cor_texto;


    document.getElementById(
        "corFundo"
    ).value =
        slide.cor_fundo;


    atualizarPreview();

}


/* ======================================
   SALVAR
====================================== */

async function salvarSlide() {

    if (!slideAtual) {

        alert(
            "Selecione um slide."
        );

        return;

    }


    const dados = {

        titulo:
            document.getElementById(
                "tituloSlide"
            ).value,

        texto:
            document.getElementById(
                "textoSlide"
            ).value,

        tamanho:
            document.getElementById(
                "tamanho"
            ).value,

        cor_texto:
            document.getElementById(
                "corTexto"
            ).value,

        cor_fundo:
            document.getElementById(
                "corFundo"
            ).value

    };


    await fetch(

        `/api/slides/${slideAtual}`,

        {

            method: "PUT",

            headers: {

                "Content-Type":
                    "application/json"

            },

            body:
                JSON.stringify(dados)

        }

    );


    await carregarSlides();

}


/* ======================================
   EXIBIR
====================================== */

function exibirSlide() {

    const dados = {

        texto:
            document.getElementById(
                "textoSlide"
            ).value,

        tamanho:
            document.getElementById(
                "tamanho"
            ).value,

        corTexto:
            document.getElementById(
                "corTexto"
            ).value,

        corFundo:
            document.getElementById(
                "corFundo"
            ).value

    };


    socket.emit(
        "exibir",
        dados
    );

}


/* ======================================
   LIMPAR
====================================== */

function limpar() {

    socket.emit(
        "limpar"
    );

}


/* ======================================
   PREVIEW
====================================== */

function atualizarPreview() {

    const preview =
        document.getElementById(
            "preview"
        );


    const texto =
        document.getElementById(
            "textoSlide"
        ).value;


    const tamanho =
        document.getElementById(
            "tamanho"
        ).value;


    const corTexto =
        document.getElementById(
            "corTexto"
        ).value;


    const corFundo =
        document.getElementById(
            "corFundo"
        ).value;


    preview.innerText =
        texto || "Digite seu texto...";


    preview.style.fontSize =
        tamanho + "px";


    preview.style.color =
        corTexto;


    preview.style.background =
        corFundo;

}


/* ======================================
   EVENTOS
====================================== */

document
    .getElementById("textoSlide")
    .addEventListener(
        "input",
        atualizarPreview
    );


document
    .getElementById("tamanho")
    .addEventListener(
        "input",
        atualizarPreview
    );


document
    .getElementById("corTexto")
    .addEventListener(
        "change",
        atualizarPreview
    );


document
    .getElementById("corFundo")
    .addEventListener(
        "change",
        atualizarPreview
    );