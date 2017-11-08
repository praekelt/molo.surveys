$(function(){
  var multi_step_checkbox = $('#id_multi_step');
  var multi_step_label = $('label[for=id_multi_step]');

  var display_direct_checkbox = $('#id_display_survey_directly');
  var display_direct_label = $('label[for=id_display_survey_directly]');

  var disableMultiStep = function(){
    multi_step_checkbox.attr("disabled", true);
    multi_step_label.css('color', 'lightgray');
  }

  var enableMultiStep = function(){
    multi_step_checkbox.attr("disabled", false);
    multi_step_label.css('color', '#333');
  }

  var disableDisplayDirect = function(){
    display_direct_checkbox.attr("disabled", true);
    display_direct_label.css('color', 'lightgray');
  }

  var enableDisplayDirect = function(){
    display_direct_checkbox.attr("disabled", false);
    display_direct_label.css('color', '#333');
  }

  if (multi_step_checkbox.is(':checked')) {
      disableDisplayDirect();
  }
  else if (display_direct_checkbox.is(':checked')) {
      disableMultiStep();
  }

  display_direct_checkbox.change(
    function(){
        if ($(this).is(':checked')) {
            disableMultiStep();
        }
        else {
          enableMultiStep();
        }
    });

  multi_step_checkbox.change(
    function(){
        if ($(this).is(':checked')) {
          disableDisplayDirect();
        }
        else {
          enableDisplayDirect();
        }
    });

  window.rules = [
    'Time Rule',
    'Day Rule',
    'Referral Rule',
    'Visit Count Rule',
    'Article Tag Rule',
    'Query Rule',
    'Device Rule',
    'User Is Logged In Rule',
    'Comment Data Rule',
    'Profile Data Rule',
    'Survey Submission Data Rule',
    'Group Membership Rule',
  ]

  window.ruleIndex = {};
  window.ruleFields = [];

  window.initRuleIndex = function(){
    rules.map(function(ruleTitle) {
      var ruleInfo = {
        ruleName: ruleTitle,
        form: $('[id*="' + ruleTitle.replace(/ /g, "").toLowerCase() + '"]').filter('ul'),
        blockIds: [],
        updateBlock: function(){
          this.blockIds = $.map(this.form.children('li').not('.deleted'), function(arg, index){
            return arg.id
          });
        },
        deleteBlock: function(id){
          var index = this.blockIds.indexOf(id);
          this.updateBlock();
          var deletedOptionValue = this.ruleName.replace(/ /g, "") + "_" + String(index);
          deleteRuleFromField(deletedOptionValue);
        },
      }
      ruleInfo.updateBlock();
      window.ruleIndex[ruleInfo.form.attr("id")] = ruleInfo;
    })
  }



  window.extractRuleInfo = function(){
    var ruleValueTextPairs = []
    $.each(ruleIndex, function(index_outer, form){
      $.each(form.blockIds, function(index_inner, value) {
        ruleValueTextPairs.push({
          "value": form.ruleName.replace(/ /g, "") + "_" + String(index_inner),
          "text": form.ruleName + " " + String(index_inner + 1),
        });
      });
    });
    return ruleValueTextPairs;
  }

  window.addUpdateTrigger = function(obj, form_id, block_id){
    obj.click(function(){
      window.deleteFromRuleIndex(form_id, block_id);
    });
  }

  window.addActionToExistingDeleteButtons = function(){
    var forms = $('[id*="rule_related-FORMS"]')
      .not("#id_surveys_combinationrule_related-FORMS")
      .filter("ul");

    forms.map(function(index, form) {
      $("#" + form.id)
        .children("li")
        .not(".deleted")
        .each(function(index, block) {
          var deleteButton = $("#" + block.id).find('button[title^="Delete"]');
          window.addUpdateTrigger(deleteButton, form.id, block.id);
        });
    });
  };

  window.deleteFromRuleIndex = function(form_id, block_id){
    var block = ruleIndex[form_id]
    block.deleteBlock(block_id);
  };

  window.attachActionToRuleCreators = function() {
    var some_rules = $('[id*="rule_related-ADD"]').filter("a").not("#id_surveys_combinationrule_related-ADD");
    $.map(some_rules, function(val, i) {
      val.addEventListener("click", function() {
          var id = $(this).attr('id');
          var form_id = id.replace('ADD', 'FORMS');
          var form = $("#" + form_id);
          var newBlock = form.children(':last');
          // upate Index of Rules
          ruleIndex[form_id].updateBlock();
          updateRuleOptions();
          // add event listener to new Delete Button
          var newDeleteButton = newBlock.find('button[title^="Delete"]');
          window.addUpdateTrigger(newDeleteButton, form.attr("id"), newBlock.attr("id"));
        }, false);
    });
  };

  var createSelectManager = function(id){
    var selectRuleField = {
      hiddenInput: $('#' + id + '_0'),
      select: $('#' + id + '_1'),
      repopulateOptions: function(){
        var ruleInfo = extractRuleInfo()
        var select = this.select;
        select.children().remove();
        select.append($("<option value=''>-------</option>"));
        $.each(ruleInfo, function(index, option) {
            select.append($('<option>', {
            "value": option["value"],
            "text": option["text"],
          }));
        });
      },
      populateSelect: function(){
        var existingValue = this.hiddenInput.val();
        this.repopulateOptions();
        if(existingValue){
          this.select.val(existingValue);
        }
        this.updateHiddenField();
      },
      updateHiddenField:function(){
        this.hiddenInput.val(this.select.val())
      },
      deleteSelect: function(optionValue){
        var existingValue = this.hiddenInput.val();

        var existingRuleType = existingValue.split("_")[0]
        var existingRuleOrder = existingValue.split("_")[1]

        var deletedRuleType = optionValue.split("_")[0]
        var deletedRuleOrder = optionValue.split("_")[1]

        //check if the value is the one being deleted
        if(existingRuleType===deletedRuleType){
          if(existingRuleOrder===deletedRuleOrder){
            this.repopulateOptions();
            this.select.val("");
            this.updateHiddenField();
          }
          else if(deletedRuleOrder<existingRuleOrder){
            var newSelectedValue = existingRuleType + "_" + String(existingRuleOrder - 1);
            this.repopulateOptions();
            this.select.val(newSelectedValue);
            this.updateHiddenField();
          }
          else{
            this.populateSelect()
          }
        }
        else{
          this.populateSelect()
        }
      }
    }
    selectRuleField.populateSelect();
    return selectRuleField
  }

  window.newRuleAdded = function(id){
    ruleFields.push(createSelectManager(id));
  };

  window.deleteRuleFromField = function(deletedOption){
    $.each(ruleFields, function(index, selectManager){
      selectManager.deleteSelect(deletedOption);
    });
  }

  window.updateRuleOptions = function(){
    $.each(ruleFields, function(index, selectManager){
      selectManager.populateSelect();
    });
  }

  // Prevent User from creating more than one rule combination
  window.addHideToRuleCombinationFunctionality = function(){
    $('#id_surveys_combinationrule_related-ADD').click(function(){
      var id = $(this).attr("id");
      var form_id = id.replace("ADD", "FORMS");
      var form = $("#" + form_id);
      var deleteButton = form
        .children(":last")
        .find('button[title^="Delete"]');
      deleteButton.click(function(){
        $("#id_surveys_combinationrule_related-ADD").toggle();
      });
      $("#id_surveys_combinationrule_related-ADD").toggle();
    });
  }
  addHideToRuleCombinationFunctionality();

  initRuleIndex();
  attachActionToRuleCreators();
  addActionToExistingDeleteButtons();
})
