<template>
    <div class="deck-detail">
        <div class="deck-code">
            <a :href="deckDetailLink" target="_blank">
                {{deck}} &nbsp;-->
            </a>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {}
    }, 
    props: {
        deck: String,
    },
    computed: {
        deckDetailLink() {
            return "https://lor.mobalytics.gg/decks/code/" + this.deck
        },
    },
}
</script>

<style>
    .deck-detail {
        width: 270px;
        /* height: 100px; */
        word-wrap: break-word;
        padding: 10px;
        background-color: var(--col-dark-grey);
        font-size: 0.9em;
    }

    a {
        color: white;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    /* @media only screen and (max-width: 768px) {
        .deck-detail {
            width: 280px;
        }
    } */
</style>