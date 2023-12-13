from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError 
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TowerManage(models.Model):
    
    _name = "tower.manage"
    _description="Tower Manage"
    
    name = fields.Char(string="Tower name")
    age = fields.Integer("Age")
    image=fields.Image("Image")
    mobile=fields.Char("Mobile Number")
    street_name=fields.Char("Street Name")
    zip_code=fields.Char("Zip Code")
    city=fields.Char("City")
    state =fields.Selection([("draft","Draft"), ("pending","Pending"), ("confirm","Confirm")],string="State", default = "draft")

# class ResConfigSettings(models.TransientModel):
#     _inherit = ['res.config.settings']

    def reset_to_draft(self):
        for rec in self:    
            rec.state="draft"
        return True

    def action_pending(self):
        for rec in self:
            rec.state="pending"
        return True

    def action_confirm(self):
        for rec in self:
            rec.state="confirm"
        return True

class ResPartner(models.Model):
    
    _inherit="res.partner"
    _description="customer"
    
    
    image = fields.Binary("Image")
    last_name = fields.Char("Last Name")
    gst_no = fields.Char("Gst No")
    skype = fields.Char("Skype")
    
    # mobile = fields.Char("Mobile Number")
    # street = fields.Text("street_name") 
    # city = fields.Char("City")
    # zip = fields.Char("Zip Code")
    # email = fields.Char("Email")
    active_customer= fields.Boolean("Active Customer")
    gender = fields.Selection([('male','Male'),('female','Female')], string='Gender')
    date_of_birth = fields.Date('Date Of Birth')
    age = fields.Integer('Age', compute='_get_age')
    document_ids = fields.One2many("document.information","partner_document_id",string="Document") 
    document_type_id = fields.Many2one("document.type", string="Document" , domain=[('document_type','=','customer')])
    total_document=fields.Integer('Total Upload Document',compute="_get_total_of_count_document")
    remark =fields.Html("Remark")

    
    @api.depends('date_of_birth')
    def _get_age(self):
        print ("COMPUTE METHOD CALLED---------------------", self)
        current_date = datetime.now().date()
        difference_in_years = 0
        for record in self:
            if record.date_of_birth:
                difference_in_years = relativedelta(current_date, record.date_of_birth).years
            record.age = difference_in_years
                                                
    @api.constrains('date_of_birth')
    def _age_constrain(self):
        print("Constrains Method Called----------------------",self)
        current_date = datetime.now().date()
        difference_in_years = 0
        for record in self:
            if record.date_of_birth:
                difference_in_years = relativedelta(current_date, record.date_of_birth).years
                if difference_in_years < 18:
                    raise UserError(f"Minimum Required Age 18 And your Age is {difference_in_years}")
    
    
    @api.depends('document_ids')
    def _get_total_of_count_document(self):
        # total_document =0
        # #print("$$$$$$$$$$$$$$",self.document_ids) 
        # for record in self.document_ids:
        #     if record.upload_file:
        #         total_document += 1
        # self.total_document = total_document
        
        self.total_document = len(self.document_ids.filtered(lambda x:x.upload_file))

    def add_wizard(self):
        return {
            'type':'ir.actions.act_window',
            'res_model':'tips.info',
            'name':'Customer',
            'view_mode':'form',
            'target':'new',
        }

    
class Towers(models.Model):
    
    _name = "towers.towers"
    _inherit = ['mail.thread']
    _description="Towers"
    
    name = fields.Char("Name")
    
    secretory_id = fields.Many2one('res.company' , string="Secretory")
    mobile_no = fields.Char("Phone Number")
    email = fields.Char("Email")
    flat_active =fields.Boolean("Active Flat")
    image = fields.Binary()
    #country = fields.Char("Conuntry")    
    # email = fields.Char("Email Id")
    address = fields.Text("Address")
    
    street_name = fields.Text("street_name") 
    city = fields.Char("City")
    zip_code = fields.Char("Zip Code")
    
    remark = fields.Html("Remark")

    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state',string='State',domain="[('country_id', '=', country_id)]")
    state_name = fields.Char(string='State Name', related='state_id.name')

    floor_ids = fields.One2many('tower.floor', 'tower_tower_id','Floors')
    emanities_ids = fields.One2many("emanities.emanities", 'tower_emanities_id',"Amenities")
 

    document_ids = fields.One2many("document.information","tower_document_id","Document") 
    # document_type_ids = fields.One2many("document.information","tower_document_id","Document" )
    # services_ids = fields.One2many("services.services","tower_services_id",string="Services")
    service_ids= fields.Many2many("services.services",string="Services")
    service_ids = fields.One2many("services.services","tower_services_id",string="Services")

    total_flats_service_maintananace = fields.Float("Total Flats Service Maintenanace",compute="get_total_flats_service_maintananace")
    total_shops_service_maintananace = fields.Float("Total Shops Service Maintenanace",compute="get_total_shops_service_maintananace")
    @api.depends('service_ids')
    def get_total_flats_service_maintananace(self):
        total_flats_service_maintananace=0
        for rec in self.service_ids:
            total_flats_service_maintananace += rec.total_flat_service_maintananace
        self.total_flats_service_maintananace = total_flats_service_maintananace  

    @api.depends('service_ids')
    def get_total_shops_service_maintananace(self):
        total_shops_service_maintananace=0
        for rec in self.service_ids:
            total_shops_service_maintananace += rec.total_shop_service_maintananace
        self.total_shops_service_maintananace = total_shops_service_maintananace

    # emanities_emanities_ids = fields.Many2many("emanities.emanities","tower_emanities_rel","tower_id","emanities_id",string ="Amenities")

    total_cost=fields.Float("Total cost",compute ="_get_amount_of_maintananace" )
    
    total_flats_maintananace=fields.Float("Total Flats Maintananace",compute ="get_total_flats_maintananace")
    total_shops_maintananace=fields.Float("Total Shops Maintananace",compute ="get_total_shops_maintananace")

    @api.depends('emanities_ids')
    def get_total_flats_maintananace(self):
        total_flats_maintananace = 0
        for rec in self.emanities_ids:
            total_flats_maintananace += rec.total_flat_maintananace
        self.total_flats_maintananace = total_flats_maintananace

    @api.depends('emanities_ids')
    def get_total_shops_maintananace(self):
        total_shops_maintananace = 0
        for rec in self.emanities_ids:
            total_shops_maintananace += rec.total_shop_maintananace
        self.total_shops_maintananace = total_shops_maintananace
    

    total_document = fields.Integer("Total Upload Documentation")

    total_flats =fields.Integer("Total Flats In Tower ", compute = "_get_total_of_flats",store=True)

    total_shops = fields.Integer("Total Shops In Tower")

    per_flat_maintananace = fields.Float("Per Flat Maintananace",compute="get_per_flat_maintananace")
    per_shop_maintananace = fields.Float("Per Shop Maintananace",compute="get_per_shop_maintananace")

    @api.depends('floor_ids')
    def get_per_flat_maintananace(self):
        per_flat_maintananace=0
        for rec in self:
            if rec.total_flats == 0:
                print("Total Flats:",rec.total_flats)
            else:
                per_flat_maintananace = (rec.total_flats_maintananace + rec.total_flats_service_maintananace)/rec.total_flats
        self.per_flat_maintananace = per_flat_maintananace

    @api.depends('floor_ids')
    def get_per_shop_maintananace(self):
        per_shop_maintananace=0
        
        for rec in self:
            if rec.total_shops == 0:
                print("Total Shops:",rec.total_shops)
            else:
                per_shop_maintananace = (rec.total_shops_maintananace + rec.total_shops_maintananace  )/rec.total_shops
        self.per_shop_maintananace = per_shop_maintananace

        
    state =fields.Selection([("draft","Draft"), ("pending","Pending"), ("confirm","Confirm")],string="State", default = "draft")
    

    def add_wizard(self):
        return {
            'type':'ir.actions.act_window',
            'res_model':'tips.info',
            'name':'Tower',
            'view_mode':'form',
            'target':'new',
        }

    def default_get(self,fields):
        print('fields...............',fields)
        print('...............',self)
        
        country_id=self.env['res.country'].search([('code','=','IN')])
        state_id=self.env['res.country.state'].search([('code','=','GJ'),('country_id','=',country_id.id)])
        
        print("state_id......country_id...",state_id,country_id)
        
        res = super(Towers,self).default_get(fields)
        
        if 'state_id' in fields:
            # res.update({'state_id': state_id})
            res['state_id'] = state_id
        if 'country_id' in fields:
            res['country_id'] = country_id
        
        res['remark']= 'Good'
        
        print("res...............",res)
        return res 
    
    def reset_to_draft(self):
        for rec in self:    
            rec.state="draft"
        return True

    def action_pending(self):
        for rec in self:
            rec.state="pending"
        return True

    def action_confirm(self):
        for rec in self:
            rec.state="confirm"
        return True
    
    @api.constrains("floor_ids")
    def _check_floor(self):
        # for rec in self:
        newlist =[]
        for i in self.floor_ids:
            if i.floor_id in newlist:
                raise ValidationError(f"You are Enter {i.floor_id.name} Floor Name More than One Time")
            elif i.floor_id.id is False:
                raise UserError("You Floor Name is Empty Please Select Floor Name ")    
            else:
                newlist.append(i.floor_id)
            
        print("New LIst+++++:",newlist)    
         
    @api.constrains("emanities_ids")
    def _check_emanities(self): 
        for rec in self:
               newlist = []
               for i in rec.emanities_ids:
                   if i.emanities_id in newlist:
                       raise UserError("You are Enter The Same Amenities More than One Time")
                   else:
                       newlist.append(i.emanities_id)
    
    
    @api.depends("floor_ids")
    def _get_total_of_flats(self):
        total_flats = 0
        print("##########",self.floor_ids)
        for record in self.floor_ids:
            total_flats += record.no_of_flats
        self.total_flats=total_flats

    @api.onchange("floor_ids")
    def _get_total_of_shops(self):
        # total_shops =0
        # print("**********",self.floor_ids)
        # for record in self.floor_ids:
        #     total_shops += record.no_of_shops
        # self.total_shops=total_shops

        for record in self:
            record.total_shops = record.floor_ids and sum(record.floor_ids.mapped('no_of_shops')) or 0


    @api.depends('emanities_ids')
    def _get_amount_of_maintananace(self):
        # total_cost = 0
        # print("**********",self.emanities_ids)
        # for record in self.emanities_ids:
        #     total_cost += record.maintananace
        # self.total_cost=total_cost    

        for record in self:
            record.total_cost = record.emanities_ids and sum(record.emanities_ids.mapped('maintananace')) or 0


    # we can use @api.depends() when use a @api.onchange()
    @api.onchange('document_ids')
    def _get_total_of_count_document(self):
        total_document =0
        #print("$$$$$$$$$$$$$$",self.document_ids) 
        for record in self.document_ids:
            if record.upload_file:
                total_document += 1
        self.total_document = total_document

        # self.total_document = len(self.document_ids.filtered(lambda x:x.upload_file))
        
        # print("Self...................:",self)      
        
        # for record in self:
        #     total_document =0
        #     print("*******")
        #     for document in record.document_ids:
        #         if document.upload_file:
        #             total_document += 1
        #     record.total_document = len(record.document_ids.filtered(lambda x:x.upload_file))
        

    def compute_document_no(self):
        for rec in self:
            rec.total_document = rec.document_ids and len(rec.document_ids) or 0
        return True
    
    def action_open_documents(self):
        return {
            'name': "Documents",
            'type': "ir.actions.act_window",
            'res_model': "document.information",
            "view_mode": "tree",
            "domain": [('id', 'in', self.document_ids.ids)],
            "context": {
                'default_tower_document_id': self.id,                
            }
        }
        
    

#  *****************************************ORM Methods***********************************************************************************************
    
    # Create Method ***************************************
    @api.model_create_multi
    def create(self,vals):
        # print("Self.......",self)
        print("Vals......",vals)
        res = super(Towers,self).create(vals)
        print("res........",res)
        for dic in vals:
            print("dic.....",dic)   
            for key in dic:
                # print("key......",key)
                if key == 'name' and not (dic['name'] != False and dic['name'].startswith("Tower")):
                    print("if ......name...............................")
                    raise UserError( "Tower Name Error")
                
                
                elif key =='remark' and dic['remark'] == False:
                    print("elif .............................................................")
                    raise UserError("Remark is Empty please Fill The Remark ")
                ''' It is not valid++++++++++++++++++++++++++++++++++++++++++++++ '''
                # elif key == 'name' and not (dic['name'].startswith("Tower")):
                #     print("Elif>>>>>>>name>>>>>>>>>")
                #     raise UserError("Enter Valid Tower Name")
                '''  *************************************************************'''
                
                
            
        print("Res>>>>>>>>>>>>>",res)        
        return res
    
    # Write Method **************************************************************************************
    def write(self,vals):
        res=super(Towers,self).write(vals)  
        print("RES>>>>>>>>>>>>>>>>:",res)
        # print("self..........",self)
        print("Vals...........",vals)
        for key in vals:
            print("key......",vals[key])
            
            if key =='name' and not vals['name'].startswith("Tower") :
                print("if ......................................")
                raise UserError("Enter The valid Tower Name \n *(start with Tower)")
        print("Res.................",res) 
        return res
     
    def update(self):
        print(" **********")   
        # search_rec = self.search([],offset=2,order='filed_name desc',limit=4)
        search_state_rec = self.search([('state_name','!=','Gujarat')])
        print("Search Rec////////////////////",search_state_rec)
        
               
        search_count_state_rec = self.search_count([('state_name','!=','Gujarat')])
        print("Search Count Rec##############################",search_count_state_rec)
        
        
        browse_state_rec = self.browse([20,91])
        print("Browse rec**************************",browse_state_rec)
    
        
        rec =self.read(['id'])
        print("id********************: ",rec)
        browse_state_rec = self.browse([rec])
        print("Loop Browse rec**************************",browse_state_rec)
            
        for rec in search_state_rec:
            read_state_rec = rec.read([])
            print("Read Rec :",read_state_rec)
        
        #  ***********************************************************************************************
        
        
# ***************************************************************************************************************************************************    

    # def wizard_add(self):
    #     print("Wizard is called..................")

    #     return {
    #         'type':'ir.actions.act_window',
    #         'res_model':'sale.info',
    #         'name':'Tower',
    #         'view_mode':'form',
    #         'target':'new',
    #     }


class Floor(models.Model):
    _name ="floor.floor"
    _description="Floor"
    name = fields.Char("Floor Number")
    code = fields.Integer("Code")
class TowerFloor(models.Model):
    _name = 'tower.floor'
    _description="Tower Floor"
    no_of_shops = fields.Integer("No Of Shops")
    no_of_flats = fields.Integer("No Of Flats")
    floor_id = fields.Many2one('floor.floor','Floor')
    tower_tower_id = fields.Many2one('towers.towers', 'Towers')
    

    
    def Add_Flats(self):
        print("&&&&&&&&&&&&&&&")
        
        rec=self.env['tower.flat'].search([('tower_id','=',self.tower_tower_id.id),('floor_id','=',self.floor_id.id)])
        rec.unlink()
        
        print("No Of Flats*****:",self.no_of_flats)
        print("No Of Shops*****:",self.no_of_shops)
        counter=0
        for flat in range(self.no_of_flats):
            counter += 1
            self.env['tower.flat'].create({'tower_id': self.tower_tower_id.id, 'floor_id': self.floor_id.id, 'type': 'flat','name':str(self.floor_id.code) + str(counter).zfill(2)})

        for shop in range(self.no_of_shops):
            counter += 1
            self.env['tower.flat'].create({'tower_id': self.tower_tower_id.id, 'floor_id': self.floor_id.id, 'type': 'shop','name':str(self.floor_id.code) + str(counter).zfill(2)})

        # for rec in range(self.no_of_flats):
        #     self.env['tower.flat'].create({'tower_id':self.tower_tower_id.id,'floor_id':self.floor_id.id,'type':'flat'})
        
        # for rec in range(self.no_of_shops):
        #     self.env['tower.flat'].create({'tower_id':self.tower_tower_id.id,'floor_id':self.floor_id.id,'type':'shop'})
        


#  **********************************Tower Flat **************************************************************************
class TowerFlat(models.Model):
    
    _name = "tower.flat"
    _description="Tower Flat"
    
    name = fields.Char("Name")
    tower_id =fields.Many2one("towers.towers",string="Tower")
    floor_id = fields.Many2one("floor.floor",string="Floor")
    type = fields.Selection([('flat','Flat'),('shop','Shop')], string="Type")
    

    


class Services(models.Model):
    
    _name = "services.services"
    _description="Services"
    
    name = fields.Char("Service Name")
    description  = fields.Text("Description")
    
    service_id =fields.Many2one("services.services","Services")
    tower_services_id = fields.Many2one("towers.towers","Services")

    services_maintananace = fields.Float("Cost of Services") 
    flat_services_maintananace = fields.Float("Total Flat Service Maintananace (%)" )
    shop_services_maintananace = fields.Float("Total Shop Service Maintananace (%)" ,compute="flat_shop_services_maintananace")

    @api.depends('flat_services_maintananace')
    def flat_shop_services_maintananace(self):
        for rec in self:
            rec.shop_services_maintananace = 1 - rec.flat_services_maintananace
            

    total_flat_service_maintananace = fields.Float("Flat Service Maintenanace ",compute="get_flat_service_maintananace")
    total_shop_service_maintananace = fields.Float("Shop Service Maintenanace",compute="get_shop_service_maintananace")
    @api.depends('services_maintananace')
    def get_flat_service_maintananace(self):
        for rec in self:
            rec.total_flat_service_maintananace = rec.services_maintananace * rec.flat_services_maintananace

    @api.depends('services_maintananace')
    def get_shop_service_maintananace(self):
        for rec in self:
            rec.total_shop_service_maintananace = rec.services_maintananace * rec.shop_services_maintananace

class Emanities(models.Model):
    
    _name = "emanities.emanities"
    _description="Amenities"
    
    name = fields.Char("Amenities")
    flat_maintananace = fields.Float("Total Flat Maintananace (%)" )
    shop_maintananace = fields.Float("Total Shop Maintananace (%)",compute="flat_shop_percentage")
    total_flat_maintananace = fields.Float("Flat Maintananace ",compute="get_flat_maintananace")
    total_shop_maintananace = fields.Float("Shop Maintananace",compute="get_shop_maintananace")

    @api.depends('maintananace')
    def get_flat_maintananace(self):
        for rec in self:
            rec.total_flat_maintananace = (rec.maintananace * rec.flat_maintananace)
    
    @api.depends('maintananace')
    def get_shop_maintananace(self):
        for rec in self:
            rec.total_shop_maintananace = rec.maintananace * rec.shop_maintananace
            

    maintananace = fields.Float("Cost of Amenities")
    emanities_id=fields.Many2one("emanities.emanities", "Ameinities")
    tower_emanities_id=fields.Many2one("towers.towers","Aeminities")

    @api.depends('flat_maintananace')
    def flat_shop_percentage(self):
        for rec in self:
                rec.shop_maintananace = 1 - rec.flat_maintananace

    # @api.onchange('flat_maintananace')
    # def total_flat_maintananace(self):

        

    # @api.onchange('shop_maintananace')
    # def flat_shop_percentage(self):
    #     for rec in self:
    #         rec.flat_maintananace = 1 - rec.shop_maintananace

class Document_Type(models.Model):
    
    _name = "document.type"
    _description="Document Type"
    
    name = fields.Char("Document Type")
    document_type=fields.Selection([('property','Property'),('customer','Customer')],string='Document')



class Document_Information (models.Model):
    
    _name="document.information"
    _description="Document Info"
    
    name = fields.Char("Document Name")
    
   
    upload_file = fields.Binary("Upload File")
    file_name = fields.Char("File name")

    document_id=fields.Many2one("document.type", "Document" )

    tower_document_id=fields.Many2one("towers.towers","Tower")
    
    partner_document_id=fields.Many2one("res.partner","Document")
