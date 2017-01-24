library(lpSolveAPI)

getinitials<-function(constraintslist,nc,sc){

	vc <- nc+ sc
	lps.model <- make.lp(0, vc) # define 3 variables, the constraints are added below
	r <- length(rankList)
	for(i in 1:sc){
		constraint <- NULL
		add.constraint(lps.model, constraintslist[[i]], ">=", 1)
	}

	#lower bound for every variable
	#add.constraint(lps.model, c(rep(c(0),nc),rep(c(1),sc)), "=", 1)
	for(i in 1:nc){
		sl <- rep(c(0), each=vc)
		sl[i] = 1
		add.constraint(lps.model, sl, ">",0.001)
	}

	#lower and upper bound for slack variables
	#sl <- rep(c(0), each=vc)
	for(i in (nc+1):vc){
		sl <- rep(c(0), each=vc)
		sl[i] = 1
		#add.constraint(lps.model, sl, "<",0.9999999)
		add.constraint(lps.model, sl, ">=",0.00001)
	}
	#add.constraint(lps.model, sl, ">=",1)
	# set objective function (default: find minimum)
	set.objfn(lps.model, rep(c(1), each=vc))  
	solve(lps.model)
	return(get.variables(lps.model))
}