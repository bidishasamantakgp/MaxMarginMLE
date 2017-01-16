
#author : Bidisha Samanta
#Using nlopt library
#TRY 1

library(R.matlab)

#Complete code #CHECKED
#Likelihood for a single hashtag
loglikModelIndividual <- function(beta, lambda_0, arrivals, k, omega_0, omega, epsilon) {

	n <- length(arrivals)
	
	beta 		<- beta
	lambda_0	<- lambda_0
	epsilon 	<- epsilon
	omega_0 	<- omega_0
	omega   	<- omega

	term_1 <- (lambda_0 / epsilon) * (exp(-epsilon * arrivals[n]) - exp(-epsilon * arrivals[1]))
	term_2 <- 0
	for(i in 1:length(k)){
  		term_2 <- term_2 + (beta /(omega_0 + (omega / k[i]))) * (exp( -(omega_0 + (omega / k[i]))* 
  			(arrivals[n] - arrivals[i])) - 1)
  	}
    
    Ai <- c(0,sapply(2:n, function(z) {
			sum(exp(-(omega_0 + omega/k[z]) * (arrivals[z] - arrivals[1:(z-1)])))
	}))	
	
	term_3 <- term_3 + sum(log(lambda_0 * exp(-epsilon*arrivals) + beta * Ai))
	
	return(-term_1 - term_2 - term_3)
}

#Complete code #CHECKED
#likelihood for the entire system Objective function
#paramsList <- list of parameters
#arrivalsList <- relative timestamps of the arrival procss
#kArrayList <- corresponding K array
#omega_0List <- list of omega_0 for hashtags
#omegaList <- omega of the parameters
#n <- number of hashtags
loglikeModelSystem <- function(paramsList, arrivalsList, kArrayList, omega_0List, omegaList, epsilon, n){
	ll <- 0
	slackVariables <- tail(paramsList, - 2*n)

	for(i in 1:n){
		ll <- ll + loglikModelIndividual(paramsList[2*i-1], paramsList[2*i], arrivalsList[i], 
			kArrayList[i], omega_0List[i], omegaList[i],epsilon)
	}
	return ll + sum(slackVariables)
}

#Complete code #Code checked
#calculate the gradient of the function
#sn = number of slack variables
#n = number of hashtags
eval_grad_objfnc <- function(sn, n, paramsList, arrivalsList, kArrayList, omega_0List, omegaList, epsilon){
	grad_vector <- NULL
	for (i in 1:n){
  		grad_vector <- c(grad_vector,gradUtilityLambda(omegaList[i], omega_0List[i], kArrayList[i], 
  			arrivalsList[i], epsilon, paramsList[2*i-1], paramsList[2*i]), gradUtilityBeta(omegaList[i], 
  			omega_0List[i], kArrayList[i], arrivalsList[i], epsilon, paramsList[2*i-1], paramsList[2*i]))
	}
	for (i in 1: sn){
		grad_vector <- c(grad_vector, 1)
	}
	return (grad_vector)
}

#Complete code #Code Checked
#calculate the contraints
eval_constraints <- function( omega_0List, omegaList, kArrayList, arrivalsList, paramsList, n, rankList ) {
	
	contraints = NULL
	slackList = tail(paramsList, -2*n)
	for (i in 1:length(rankList)){
		
		id1 = rankList[[i]][[1]]
		id2 = rankList[[i]][[2]]

		ts = rankList[[i]][[3]]
		te = rankList[[i]][[4]]
		
		slack = rankList[[i]][[5]]

		a1 = calculate_coef_lambda(epsilon, ts, te)
		b1 = calculate_coef_beta(omegaList[id1], omega_0List[id1], kArrayList[id1], arrivalsList[id1], ts, te)
		a2 = calculate_coef_lambda(epsilon, ts, te)
		b2 = calculate_coef_beta(omegaList[id2], omega_0List[id2], kArrayList[id2], arrivalsList[id2], ts, te)

		constraints = rbind(constriants,(1 - slackList[slack] + a1 * paramsList[2*id1-1] + b1 * paramsList[2*id1] - 
			a2 * paramsList[2*id2-1] - b2 * paramsList[2*id2])
	}
	return contraints
}


#Code complete #Code checked
#calculate the gradient of the contriant function
#n = number of hashtag
#sn = number of slack variables
eval_grad_contrains <-function(rules, n, sn){
	gradchain = NULL
	for (i in 1:rules){
		id1 = rankList[i][1]
		id2 = rankList[i][2]

		ts = rankList[i][3]
		te = rankList[i][4]
		
		slack = rankList[i][5]

		a1 = calculate_coef_lambda(epsilon, ts, te)
		b1 = calculate_coef_beta(omegaList[id1], omega_0List[id1], kArrayList[id1], arrivalsList[id1], ts, te)
		a2 = calculate_coef_lambda(epsilon, ts, te)
		b2 = calculate_coef_beta(omegaList[id2], omega_0List[id2], kArrayList[id2], arrivalsList[id2], ts, te)

		aList = NULL
		bList = NULL
		slackList = NULL

		for (j in 1:n){
			if (id1==j){
				aList = c(aList, a1, b1)
			} 
			else if(id2 == j){
				aList = c(aList, a2, b2)
			}
			else{
				aList = c(aList, 0, 0)
			}
		}
		for (j in 1:sn){
			if(slack == j){
				slackList = c(slackList, -1)
			}
			else {
				slackList = c(slackList, 0)
			}
		}
		gradchain = rbind(gradchian, c(aList, slackList))
	}
	return gradchain
}

#main Block

myArgs <- commandArgs(trailingOnly = TRUE)

fileName <- myArgs[1]
rankfileName <- myArgs[2]

parameters <- parseParams(fileName)
rankconstraints <- parseRank(rankfileName)
rankList <-parseRank(rankfileName)

res0 <- nloptr( x0=x0 ,eval_f=eval_grad_objfnc, eval_grad_f=eval_grad_f0, 
	eval_g_ineq = eval_g0, eval_jac_g_ineq = eval_jac_g0, opts = list("algorithm" = "NLOPT_LD_MMA", 
	"print_level" = 2, "check_derivatives" = TRUE, "check_derivatives_print" = "all"), arrivalsList = arrivalsList, 
	kArrayList = kArrayList, omega_0List = omega_0List, omegaList = omegaList, epsilon = epsilon, n = n)

writeFileName <- myArgs[2]
