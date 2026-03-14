<template>
	<v-row align="center" class="items px-2 py-1 mt-0 compact-row" no-gutters v-if="pos_profile.posa_allow_change_posting_date">
		<v-col cols="12" sm="6" class="pb-0">
			<VueDatePicker
				ref="postingDatePicker"
				v-model="internal_posting_date_display"
				model-type="format"
				format="dd-MM-yyyy"
				auto-apply
				teleport
				:placeholder="placeholderText"
				class="sleek-field posting-date-input pos-themed-input"
				@update:model-value="onUpdate"
			/>
		</v-col>
		<v-col
			v-if="pos_profile.posa_enable_price_list_dropdown"
			cols="12"
			sm="6"
			class="pb-0 d-flex align-center posting-meta-col compact-balance-col"
		>
			<v-select
				density="compact"
				variant="solo"
				color="primary"
				:items="priceLists"
				:placeholder="priceListLabel"
				single-line
				v-model="internal_price_list"
				hide-details
				class="flex-grow-1 sleek-field"
				@update:model-value="onPriceListUpdate"
			/>
			<div v-if="pos_profile.posa_show_customer_balance" class="balance-field ml-3">
				<strong class="balance-label">{{ __("Balance") }}:</strong>
				<span class="balance-value">{{ formatCurrency(customer_balance) }}</span>
			</div>
		</v-col>
		<v-col
			v-else-if="pos_profile.posa_show_customer_balance"
			cols="12"
			sm="6"
			class="pb-0 d-flex align-center posting-meta-col compact-balance-col"
		>
			<div class="balance-field">
				<strong class="balance-label">{{ __("Balance") }}:</strong>
				<span class="balance-value">{{ formatCurrency(customer_balance) }}</span>
			</div>
		</v-col>
	</v-row>
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";
import type { POSProfile } from "../../../types/models";

interface Props {
	pos_profile: POSProfile | any; // Loose typing for now to avoid breaking changes
	posting_date_display?: string;
	customer_balance?: number;
	formatCurrency: (_val: number | undefined) => string;
	priceList?: string;
	priceLists?: string[];
}

const props = defineProps<Props>();

const __ = (str: string) => (window.__ ? window.__(str) : str);

const emit = defineEmits<{
	"update:posting_date_display": [val: string];
	"update:priceList": [val: string];
}>();

const internal_posting_date_display = ref(props.posting_date_display);
const internal_price_list = ref(props.priceList);
const postingDatePicker = ref<any>(null);

const placeholderText = computed(() => frappe._("Posting Date"));
const priceListLabel = computed(() => frappe._("Price List"));

watch(
	() => props.posting_date_display,
	(val) => {
		internal_posting_date_display.value = val;
	},
);

watch(
	() => props.priceList,
	(val) => {
		internal_price_list.value = val;
	},
);

const onUpdate = (val: any) => {
	emit("update:posting_date_display", val);
};

const onPriceListUpdate = (val: any) => {
	emit("update:priceList", val);
};

const focusPostingDate = () => {
	// Use optional chaining carefully with the ref
	const el = postingDatePicker.value?.$el || postingDatePicker.value;
	const input = el?.querySelector("input");
	if (input) {
		input.focus();
		input.select?.();
	}
};

// Expose methods for template refs
defineExpose({
	focusPostingDate,
});
</script>

<style scoped>
/* Theme-aware input styling */
.posting-date-input :deep(.v-field__input),
.posting-date-input :deep(input),
.posting-date-input :deep(.v-label) {
	color: var(--pos-text-primary) !important;
}

.posting-date-input :deep(.v-field__overlay) {
	background-color: var(--pos-input-bg) !important;
}

/* Theme-aware date picker elements */
:deep(.dp__input) {
	background-color: var(--pos-input-bg) !important;
	color: var(--pos-text-primary) !important;
}

:deep(.dp__menu) {
	background-color: var(--pos-card-bg) !important;
	color: var(--pos-text-primary) !important;
	z-index: 4000 !important;
}

.compact-row {
	min-height: 42px;
}

.posting-meta-col {
	justify-content: flex-end;
}

.compact-balance-col {
	gap: 8px;
}

.balance-field {
	margin-left: auto;
	text-align: right;
	font-size: 0.78rem;
	white-space: nowrap;
}

.balance-label {
	font-size: 0.78rem;
}

.balance-value {
	font-size: 1rem;
	font-weight: 700;
	margin-left: 4px;
}

/* Ensure calendar numbers remain visible across themes */
.posting-date-input :deep(.dp__calendar_header_item),
.posting-date-input :deep(.dp__cell_inner) {
	color: var(--pos-text-primary) !important;
}

/* Sleek design for VueDatePicker */
:deep(.sleek-field) .dp__input_wrap {
	width: 100%;
	box-sizing: border-box;
}

:deep(.sleek-field) .dp__input {
	width: 100%;
	border-radius: 8px;
	box-shadow: none;
	transition: box-shadow 0.2s ease;
	background-color: var(--field-bg);
	color: var(--text-primary);
	padding: 6px 32px 6px 10px;
	min-height: 36px;
}

:deep(.sleek-field:hover) .dp__input {
	box-shadow: none;
}

/* Align calendar icon to the right, before the clear icon */
.posting-date-input :deep(.dp__input_icon) {
	inset-inline-start: auto;
	inset-inline-end: 30px;
}

/* Remove extra left padding added for left icon placement */
.posting-date-input :deep(.dp__input_icon_pad) {
	padding-inline-start: 12px;
}

/* Increase right padding to accommodate both icons */
.posting-date-input :deep(.dp__input) {
	padding-right: calc(30px + var(--dp-input-icon-padding));
}

:deep(.v-field),
:deep(.v-field__input) {
	min-height: 36px !important;
}

:deep(.v-label) {
	display: none !important;
}
</style>
