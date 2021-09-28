<template>
    <div class="locale-changer">
        <div class="title">
            {{$t('str.languages')}}
        </div>
        <div class="select-container">
            <select v-model="$i18n.locale">
                <option v-for="locale in $i18n.availableLocales" :key="`locale-${locale}`" :value="locale">{{ locale }}</option>
            </select>
        </div>
    </div>
</template>

<style scoped>
    .locale-changer {
        display: flex;
        justify-content: space-between;
        width: 100%;
    }

    select {
        font-size: 0.9em;
        outline: none;
        background: var(--col-dark-grey);
        color: white;
        padding: 8px 20px 8px 15px;
        border-radius: 40px;
        border: 0px;
        appearance: none;
        cursor: pointer;
    }

</style>