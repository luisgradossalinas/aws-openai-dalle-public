# AWS integration with Dall-e (OpenAI) and WhatsApp

<img width="900" src="https://user-images.githubusercontent.com/2066453/235762189-ece5ec56-84aa-4fc3-97fe-0e265a69d36f.png">

## Requisitos

- [Tener una cuenta en AWS](https://gist.github.com/luisgradossalinas/c233c0333022c6617dd70609bfdf6441)
- [Tener una cuenta en OpenAI](https://gist.github.com/luisgradossalinas/45c1c5ed27b7f73e0d3cf3bc0fbe846d)
- [Tener una cuenta en UltraMSG](https://gist.github.com/luisgradossalinas/1380c0b42f85ed3a46e7e9ede4249f09)

## Accedemos a nuestra cuenta de AWS y creamos un entorno de Cloud9, donde clonaremos el repositorio.

Ejecutar en Cloud9.

	git clone https://github.com/luisgradossalinas/aws-openai-dalle-public

Abrir el contenido del archivo falle.yaml e ingresamos en la línea 66 nuestro API Key de OpenAI.

<img width="900" src="https://user-images.githubusercontent.com/2066453/235765642-9e08e73a-7495-414d-bfc9-6712c19bdbda.png">

En la línea 73, ingresar el valor de nuestra instancia y token de UltraMsg.

Ejecutar en Cloud9

	cd aws-openai-dalle-public
	sh sh/01_Start_Deploy.sh

Esperamos que se cree el stack en CloudFormation.

Una vez creado el stack, ejecutamos en Cloud9 lo siguiente para iniciar la aplicación web en Flask.

	python3 web/app.py

Abrimos el puerto 8081, de la EC2 (Añadir una regla de entrada al Security group).

<img width="600" src="https://user-images.githubusercontent.com/2066453/235768344-4bdb3628-3c4c-4119-988d-023714b83c55.png">

Añadir la regla de entrada.

<img width="800" src="https://user-images.githubusercontent.com/2066453/235768523-3989a9bd-882b-4e64-a9c0-a1ea0832d9ec.png">

Abrimos un navegador y pegamos la IP pública de la EC2 concatenada con el puerto 8081

Abrimos un nuevo terminal en Cloud9 y ejecutamos lo siguiente:

	curl -s http://checkip.amazonaws.com | awk {'print "http://" $1 ":8081"'}
	
Pegar el resultado en un navegador y veremos la siguiente página.

<img width="800" src="https://user-images.githubusercontent.com/2066453/235770651-bfd15ec9-618d-4ef7-a45f-c7e0e40bac6a.png">

<img width="800" src="https://user-images.githubusercontent.com/2066453/235770977-94bdad22-57d1-473d-9fc2-c2c03dc94938.png">

<img width="800" src="https://user-images.githubusercontent.com/2066453/235771210-d6df0128-375c-41da-9ba8-e3270903ba10.png">

<img width="491" src="https://user-images.githubusercontent.com/2066453/235746691-7b926dd2-56d9-4451-a53f-17591494b3aa.png">

## Documentación

https://realpython.com/generate-images-with-dalle-openai-api

https://github.com/openai/openai-cookbook/blob/main/examples/dalle/Image_generations_edits_and_variations_with_DALL-E.ipynb

## Agradecimientos

Espero te haya servido esta solución, si pudiste replicarlo, puedes publicarlo en LinkedIn con tus aportes, cambios y etiquétame (https://www.linkedin.com/in/luisgrados).

## Eliminar recursos en AWS

Ejecutamos en Cloud9.

    aws s3 ls | grep dalle-images | awk {'print "aws s3 rb s3://" $3 " --f"'} | sh
    aws s3 ls | grep dalle-code | awk {'print "aws s3 rb s3://" $3 " --f"'} | sh   
    aws cloudformation delete-stack --stack-name StackDalle
    echo "Stack StackDalle eliminándose"
