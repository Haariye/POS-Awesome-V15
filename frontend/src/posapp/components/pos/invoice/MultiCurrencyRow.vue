<template>
	<v-row align="center" class="items px-2 py-1 mt-0 compact-row" no-gutters v-if="pos_profile.posa_allow_multi_currency">
		<v-col cols="12" sm="4" class="pb-0 px-1">
			<v-select
				density="compact"
				variant="solo"
				color="primary"
				:placeholder="currencyLabel"
				single-line
				class="pos-themed-input sleek-field"
				hide-details
				v-model="internal_selected_currency"
				:items="available_currencies"
				@update:model-value="onCurrencyUpdate"
			></v-select>
		</v-col>
		<v-col cols="12" sm="4" class="pb-0 px-1">
			<v-text-field
				density="compact"
				variant="solo"
				color="primary"
				:placeholder="priceListLabel"
				single-line
				class="pos-themed-input sleek-field"
				hide-details
				v-model="internal_plc_rate"
				:rules="[isNumber]"
				@change="onPlcRateChange"
			></v-text-field>
		</v-col>
		<v-col cols="12" sm="4" class="pb-0 px-1">
			<v-text-field
				density="compact"
				variant="solo"
				color="primary"
				:placeholder="conversionRateLabel"
				single-line
				class="pos-themed-input sleek-field"
				hide-details
				v-model="internal_conversion_rate"
				:rules="[isNumber]"
				@change="onConversionChange"
			></v-text-field>
		</v-col>
	</v-row>
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";
import type { POSProfile } from "../../../types/models";

interface Props {
	pos_profile: POSProfile | any;
	selected_currency?: string;
	plc_conversion_rate?: number;
	conversion_rate?: number;
	available_currencies?: string[];
	isNumber: (_val: any) => boolean | string;
	price_list_currency?: string;
}

const props = defineProps<Props>();

const emit = defineEmits<{
	(_e: "update:selected_currency", _val: string): void;
	(_e: "update:plc_conversion_rate", _val: number | undefined): void;
	(_e: "update:conversion_rate", _val: number | undefined): void;
}>();

const internal_selected_currency = ref(props.selected_currency);
const internal_plc_rate = ref(props.plc_conversion_rate);
const internal_conversion_rate = ref(props.conversion_rate);

const currencyLabel = computed(() => frappe._("Currency"));
const conversionRateLabel = computed(() => frappe._("Conversion Rate"));
const priceListLabel = computed(
	() => "Price List " + props.price_list_currency + " to " + internal_selected_currency.value,
);

watch(
	() => props.selected_currency,
	(val) => {
		internal_selected_currency.value = val;
	},
);

watch(
	() => props.plc_conversion_rate,
	(val) => {
		internal_plc_rate.value = val;
	},
);

watch(
	() => props.conversion_rate,
	(val) => {
		internal_conversion_rate.value = val;
	},
);

const onCurrencyUpdate = (val: any) => {
	emit("update:selected_currency", val);
};

const onPlcRateChange = () => {
	emit("update:plc_conversion_rate", internal_plc_rate.value);
};

const onConversionChange = () => {
	emit("update:conversion_rate", internal_conversion_rate.value);
};
</script>

<style scoped>
.compact-row {
	min-height: 42px;
}

:deep(.v-field),
:deep(.v-field__input) {
	min-height: 36px !important;
}

:deep(.v-label) {
	display: none !important;
}
</style>
