/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global isDomElem */

/* Get the input mask element for an input */
/* Requires: */
/*  inputElem: Input element who's input mask is required */
function getMask(inputElem) {
    let inputMask;
    if (isDomElem(inputElem) === true) {
        inputMask = $(inputElem).closest('.input-mask-wrapper').
            find('.input-mask');
        if (inputMask.length > 0) {
            return inputMask;
        }
    }
    return false;
}

/* Horizontally position an input mask */
/* Requires: */
/*  inputElem: Input element who's mask should be updated */
// eslint-disable-next-line no-unused-vars
function updateMask(inputElem) {
    let inputMask = getMask(inputElem);
    let inputValue;
    let maskWidth;
    let inputStartPadding;
    let adjustedPadding;
    if (inputMask !== false) {
        inputValue = $(inputMask).find('.input-value');
        if ($(inputValue).length > 0) {
            $(inputValue).html($(inputElem).val());
            return;
        }
        $(inputElem).removeClass('adjust-start-padding-for-mask');
        maskWidth = parseFloat($(inputMask).find('.input-mask-value').
            outerWidth());
        inputStartPadding = parseFloat($(inputElem).css('padding-left'));
        adjustedPadding = parseFloat(maskWidth + inputStartPadding + 4) + 'px';
        $(':root').css('--adjust-start-padding-for-mask', adjustedPadding);
        $(inputElem).addClass('adjust-start-padding-for-mask');
    }
}

/* Vertically center a mask over it's input element, then updateMask */
/* Requires: */
/*  inputElem: Input element who's input mask should be positioned */
function positionMask(inputElem) {
    let inputMaskPositioner = $(inputElem).closest('.input-mask-wrapper').
        find('.input-mask .input-mask-positioner');
    let halfInput = $(inputElem).outerHeight(true) / 2;
    let halfMask = $(inputMaskPositioner).outerHeight(true) / 2;
    $(inputMaskPositioner).css('top', -Math.abs(halfInput + halfMask));
    updateMask($(inputElem));
}

/* Add an input mask to an input */
/* Requires: */
/*  inputElem: Input element to which the mask will be added */
/*  mask: String containing characters to be used for the mask. */
/* Optional: */
/*  leadingMask: Boolean (default = false).  By default masks are placed at */
/*               the end of the input text.  Setting this to true will place */
/*               the mask at the start of the text. */
/*  maskId: String representing an element Id to be applied to the input mask */
/*          NB: If no maskId is provided, an Id will be created from the Id */
/*              attribute of the input element (if it is set), otherwise no */
/*              Id will be applied */
/*  extraClasses: List containing additional classes to be applied to the */
/*                input-mask-positioner element */
// eslint-disable-next-line no-unused-vars
function addMask({inputElem, mask, leadingMask = false, maskId, extraClasses}) {
    if (!isDomElem(inputElem)) {
        return;
    }

    if (!mask) {
        return;
    }

    $(inputElem).wrap(
        '<span class="input-mask-wrapper d-block"></span>');

    let inputValue = `<span class="input-value"></span>
    `;
    if (leadingMask === true) {
        inputValue = '';
    }

    $(inputElem).closest('.input-mask-wrapper').
        append(`
        <div class="input-mask position-relative pe-none">
            <span class="input-mask-positioner border-0 p-0 d-block w-100 ` +
            `position-absolute overflow-hidden text-nowrap">
                ` + inputValue +
                `<span class="input-mask-value">${mask}</span>
            </span>
        </div>
        `);

    if (!maskId) {
        if ($(inputElem).attr('id').length > 0) {
            maskId = $(inputElem).attr('id') + '_input_mask';
        }
    }

    let inputMask = $(inputElem).closest('.input-mask-wrapper').
        find('.input-mask');

    if (maskId.length > 0) {
        $(inputMask).attr('id', maskId);
    }

    let inputPaddingStart = parseFloat($(inputElem).css('padding-left'));
    let inputPaddingEnd = parseFloat($(inputElem).css('padding-right'));
    $(inputMask).css('margin-left', inputPaddingStart + 'px');
    if ($(inputElem).attr('type').
            toLowerCase() === 'number') {
        inputPaddingEnd += 20;
    }
    $(inputMask).css('margin-right', inputPaddingEnd + 'px');

    let inputMaskPositioner = $(inputMask).find('.input-mask-positioner');

    if (extraClasses && Array.isArray(extraClasses)) {
        extraClasses.forEach((clss) => {
            $(inputMaskPositioner).addClass(clss);
        });
    }

    positionMask(inputElem);
}

/* Hide an input mask */
/* Requires: */
/*  inputElem: Input element who's mask should be hidden */
// eslint-disable-next-line no-unused-vars
function hideMask(inputElem) {
    let inputMask = getMask(inputElem);
    let inputValue;
    if (inputMask !== false) {
        $(inputMask).find('.input-mask-positioner').
            addClass('d-none');
        inputValue = $(inputMask).find('.input-value');
        if ($(inputValue).length > 0) {
            return;
        }
        $(inputElem).removeClass('adjust-start-padding-for-mask');
    }
}

/* Show an input mask */
/* Requires: */
/*  inputElem: Input element who's mask should be shown */
// eslint-disable-next-line no-unused-vars
function showMask(inputElem) {
    let inputMask = getMask(inputElem);
    let inputValue;
    if (inputMask !== false) {
        $(inputMask).find('.input-mask-positioner').
            removeClass('d-none');
        inputValue = $(inputMask).find('.input-value');
        if ($(inputValue).length > 0) {
            return;
        }
        updateMask(inputElem);
    }
}