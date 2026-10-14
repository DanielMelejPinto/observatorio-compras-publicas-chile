SELECT 
    "Codigo" AS codigo,
    "Nombre" AS nombre,
    "CodigoEstado" AS codigo_estado,
    CASE 
        WHEN "CodigoEstado" = 12 THEN 'Recepcion Conforme'
        WHEN "CodigoEstado" = 8  THEN 'Aceptada'
        WHEN "CodigoEstado" = 9  THEN 'Cancelada'
        WHEN "CodigoEstado" = 4  THEN 'Enviada al Proveedor'
        ELSE 'Otro Estado'
    END AS descripcion_estado
FROM public.ordenes_brutas