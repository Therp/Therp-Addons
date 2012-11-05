openerp.trp_web_treeview_html_widget=function(openerp)
{
    var format_cell_org=openerp.web.format_cell;
    openerp.web.format_cell=function(row_data, column, options)
    {
        if(column.widget=='trp_treeview_html')
        {
            return row_data[column.id].value;
        }
        else
        {
            return format_cell_org(row_data, column, options);
        }
    }
}
