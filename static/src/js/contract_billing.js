openerp.contract_billing = function (instance) {
    var _t = instance.web._t;
    var _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    
    instance.web.contract_billing = instance.web.contract_billing || {};

    instance.contract_billing.selection_modify = instance.web.form.FormWidget.extend({
	    init: function (field_manager, node) {
	    	this._super(field_manager, node);
	    },
	    start:function() {
			 this._super();
			 var self = this;
			 console.log(self.field_manager);
//			 self.field_manager.on("change:actual_mode", self, function(){
//				 if (self.field_manager.get("actual_mode") == "edit"){
//					 console.log("The actual_mode is edit mode");
//					 if (this.field_manager.get_field_value("project_id")){
//						 var project_id = this.field_manager.get_field_value("project_id");
//						 var mod = new instance.web.Model("project.task");
//						 mod.call('check_contract',[self.view.datarecord.id,project_id]).done(function(ctx){
//							 if (!('cancel' in ctx)){
//								 console.log ("A contract is attached to the project");
//								 if (ctx['fix'] == false && ctx['variable'] == true && $( "select[name='type_billing']" )[0]){
//									 $( "select[name='type_billing']" )[0].children[0].disabled = true;
//									 $( "select[name='type_billing']" )[0].children[2].disabled = true;
//								 }
//								 if (ctx['fix'] == true && ctx['variable'] == false && $( "select[name='type_billing']" )[0]){
//									 $( "select[name='type_billing']" )[0].children[0].disabled = true;
//									 $( "select[name='type_billing']" )[0].children[3].disabled = true;
//								 }
//								 if (ctx['fix'] == false && ctx['variable'] == false && $( "select[name='type_billing']" )[0]){
//									 $( "select[name='type_billing']" )[0].children[0].disabled = true;
//									 $( "select[name='type_billing']" )[0].children[2].disabled = true;
//									 $( "select[name='type_billing']" )[0].children[3].disabled = true;
//								 }
//							 }
//						 });
//   				 	 }
//				 }
//			 });
			 self.field_manager.on("field_changed:id",self,function(){
				 if (self.field_manager.get("actual_mode") == "edit"){
					 try {
						 self.field_manager.on("field_changed:project_id",self,function(){
							 for (i = 0 ;i<=3;i++){
								 if ($( "select[name='type_billing']" )[0]){
									 $( "select[name='type_billing']" )[0].children[i].disabled = false
								 }
							 }
							 console.log("The id of the project chosen is ",this.field_manager.get_field_value("project_id"));
							 if (this.field_manager.get_field_value("project_id")){
								 var project_id = this.field_manager.get_field_value("project_id");
								 var mod = new instance.web.Model("project.task");
								 mod.call('check_contract',[self.view.datarecord.id,project_id]).done(function(ctx){
									 if (!('cancel' in ctx)){
										 console.log ("A contract is attached to the project");
										 if (ctx['fix'] == false && ctx['variable'] == true && $( "select[name='type_billing']" )[0]){
											 $( "select[name='type_billing']" )[0].children[0].disabled = true;
											 $( "select[name='type_billing']" )[0].children[2].disabled = true;
										 }
										 if (ctx['fix'] == true && ctx['variable'] == false && $( "select[name='type_billing']" )[0]){
											 $( "select[name='type_billing']" )[0].children[0].disabled = true;
											 $( "select[name='type_billing']" )[0].children[3].disabled = true;
										 }
										 if (ctx['fix'] == false && ctx['variable'] == false && $( "select[name='type_billing']" )[0]){
											 $( "select[name='type_billing']" )[0].children[0].disabled = true;
											 $( "select[name='type_billing']" )[0].children[2].disabled = true;
											 $( "select[name='type_billing']" )[0].children[3].disabled = true;
										 }
									 }
								 });
		   				 	 }
						 });
					 }
					 catch(err){
						 console.log("Error Averted");
					 }
				 }
			 });
		
			 try {
				 self.field_manager.on("field_changed:project_id",self,function(){
					 for (i = 0 ;i<=3;i++){
						 if ($( "select[name='type_billing']" )[0]){
							 $( "select[name='type_billing']" )[0].children[i].disabled = false
						 }
					 }
					 console.log("The id of the project chosen is ",this.field_manager.get_field_value("project_id"));
					 if (this.field_manager.get_field_value("project_id")){
						 var project_id = this.field_manager.get_field_value("project_id");
						 var mod = new instance.web.Model("project.task");
						 mod.call('check_contract',[self.view.datarecord.id,project_id]).done(function(ctx){
							 if (!('cancel' in ctx)){
								 console.log ("A contract is attached to the project",ctx);
								 if (ctx['fix'] == false && ctx['variable'] == true && $( "select[name='type_billing']" )[0]){
								 	 console.log($( "select[name='type_billing']" )[0].children[2]);
								 	 $( "select[name='type_billing']" )[0].children[0].disabled = true;
									 $($( "select[name='type_billing']" )[0].children[2]).prop('disabled',true);
									 console.log($( "select[name='type_billing']" )[0].children[2]);
								 }
								 if (ctx['fix'] == true && ctx['variable'] == false && $( "select[name='type_billing']" )[0]){
									 $( "select[name='type_billing']" )[0].children[0].disabled = true;
									 $( "select[name='type_billing']" )[0].children[3].disabled = true;
									 
								 }
								 if (ctx['fix'] == false && ctx['variable'] == false && $( "select[name='type_billing']" )[0]){
									 $( "select[name='type_billing']" )[0].children[0].disabled = true;
									 $( "select[name='type_billing']" )[0].children[2].disabled = true;
									 $( "select[name='type_billing']" )[0].children[3].disabled = true;
									 
								 }
							 }
						 });
   				 	 }
				 });
			 }
			 catch(err){
				 console.log("Error Averted");
			 }
		 },
	});
    instance.web.form.custom_widgets.add('selections', 'instance.contract_billing.selection_modify');
    instance.web.views.add('tree_invoice_task', 'instance.web.contract_billing.InvoiceTaskListView');
    instance.web.contract_billing.InvoiceTaskListView = instance.web.ListView.extend({
        init: function() {
        	this._super.apply(this, arguments);
            var self = this;
        },

        do_search: function(domain, context, group_by) {
        	var self = this;
            this.last_domain = domain;
            this.last_context = context;
            this.last_group_by = group_by;
            this.old_search = _.bind(this._super, this);
            var mod = new instance.web.Model("account.analytic.line", context, domain);
            return mod.call("list_lines_to_invoice", []).then(function(result) {
            	console.log (self.search_by_partner(result));
            	self.search_by_partner(result);            	
        	});
            
        },

        search_by_partner: function(result) {
        	this.lines = result;
        	var self = this;
        	domain = []
        	domain.push(["id", "in", self.lines]);
        	console.log(self.last_domain);
        	var compound_domain = new instance.web.CompoundDomain(self.last_domain, domain);
            var fct = function() {
        	return self.old_search(compound_domain, self.last_context, self.last_group_by);
            };
            return fct();
        },
 
        do_select: function (ids, records) {
            this.trigger('record_selected')
            this._super.apply(this, arguments);
        },
    });
};
