-- Llenar la tabla docentes_docente
insert into docentes_docente (legajo, partner_id) (
	select legajo, id 
	from res_partner 
	where id not in (select partner_id from docentes_docente)
	and esdocente = True
	and legajo is not null
	and legajo > 0
);

-- Cargar docente_bis en las solicitudes
--update docentes_solicitudes ds set docente_bis = (
--	select id from docentes_docente dd where dd.partner_id = docente
--);
