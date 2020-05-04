CREATE or REPLACE FUNCTION mapearEstado(estado varchar, valor varchar) RETURNS varchar AS $$
DECLARE 
	result varchar;
BEGIN
	if estado = 'aporto' then
		if valor = 'none' then result := 'NACA';
		elsif valor = 'baja' then result := 'NACA';
		elsif valor = 'hist' then result := 'HCA';
		elsif valor = 'pasivo' then result := 'PCA';
		elsif valor = 'pend_a' then result := 'PACA';
		elsif valor = 'pend_b' then result := 'PBCB';
		elsif valor = 'jub' then result := 'JPCA';
		elsif valor = 'becarie' then result := 'BPCA';
		elsif valor = 'contratade' then result := 'CPCA';
		else result := 'OTRA';
		end if;
	elsif estado = 'no_aporto' then
		if valor = 'activo' then result := 'ASA';
		elsif valor = 'pend_a' then result := 'PASA';
		elsif valor = 'pend_b' then result := 'PBSA';
		elsif valor = 'juba' then result := 'JASA';
		elsif valor = 'becariea' then result := 'BASA';
		elsif valor = 'contratadea' then result := 'CASA';
		else result := 'OTRA';
		end if;
	end if;
RETURN result;
END; $$
LANGUAGE PLPGSQL;


CREATE or REPLACE FUNCTION calcularInconsistencias(estado_aporte varchar, desde date, hasta date, descripcion varchar)  RETURNS integer AS $$
DECLARE 
	result integer;
BEGIN 
    if estado_aporte = 'no_aporto' then
			insert into docentes_gestion_de_cambios (docente, situacion, fecha_desde, fecha_hasta, fecha_consulta, descripcion) 
				select p.id, (select mapearEstado('no_aporto', p.estado)), desde, hasta, now(), descripcion  
				from res_partner p 
				where p.estado in ('activo', 'pend_a', 'pend_b', 'juba', 'becariea', 'contratadea') and p.id not in (
					select a.docente 
					from docentes_aportes a 
					where a.fecha between desde and hasta 
					group by a.docente);
			
			GET DIAGNOSTICS result = ROW_COUNT;
			
		elsif estado_aporte = 'aporto' then
			insert into docentes_gestion_de_cambios (docente, situacion, fecha_desde, fecha_hasta, fecha_consulta, descripcion) 
				select p.id, (select mapearEstado('aporto', p.estado)), desde, hasta, now(), descripcion    
					from res_partner p 
					where p.estado in ('none','baja','hist','pasivo','pend_a','pend_b','jub','becarie','contratade') and p.id in (
						select a.docente 
						from docentes_aportes a 
						where a.fecha between desde and hasta 
						group by a.docente);
						
			GET DIAGNOSTICS result = ROW_COUNT;
		end if;
RETURN result;
END; $$
LANGUAGE PLPGSQL;