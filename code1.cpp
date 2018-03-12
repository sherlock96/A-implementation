#include <stdio.h>
#include <stdlib.h>

// triplet of Cannibals at West Bank, Missionaries at West Bank,place of Boat(0-West 1-East) 
struct Node 
{
    int cw,mw,dir;

};
struct Node state[32];  //Max possible states = 4*4*2
int top=-1;


void push(int cw, int mw, int dir)
{   top++;
    state[top].cw=cw;
    state[top].mw=mw;
    state[top].dir=dir;
}

//Check if move from ith state to jth state is possible or not 
int move(int i, int j)
{
int cw1,mw1,cw2,mw2;
cw1=state[i].cw;
mw1=state[i].mw;
cw2=state[j].cw;
mw2=state[j].mw;


//from i to j
   if(state[i].dir==1&&state[j].dir==0){


   		if(cw1-cw2==-1 && mw1-mw2==-1) return 1;

		if(cw1-cw2==0 && mw1-mw2==-1 ) return 1;

		if(cw1-cw2==0 && mw1-mw2==-2)return 1;

		if(cw1-cw2==-1 && mw1-mw2==0)  return 1;

		if(cw1-cw2==-2 && mw1-mw2==0 )return 1;
	     
   }
//from j to i
   else if(state[i].dir==0&&state[j].dir==1){

		if(cw1-cw2==1 && mw1-mw2==1) return 1;  

		if(cw1-cw2==0 && mw1-mw2==1) return 1;

		if(cw1-cw2==0 && mw1-mw2==2) return 1;

		if(cw1-cw2==1 && mw1-mw2==0) return 1;

		if(cw1-cw2==2 && mw1-mw2==0) return 1;

	}   

    return 0;
}

//to check if state present in the given list 
int inList(int *arr, int n, int top)
{
    int i, flag=0;
    for(i=0;i<=top;i++)
    {
        if(arr[i]==n)
        {
            flag=1;
            break;
        }
    }
    return flag;
}

//DFS to reach goal state 
int DFS()
{	
    int closed[top+1],open[top+1],parent[top+1],path[top+1]; 
    
    int i, temp,j;
    for(i=0;i<=top;i++)
        {closed[i]=0; parent[i]=-1;}
	int op=-1, cl=-1, pa=-1;
    int start=0, goal=top; //start = 3 3 0   goal = 0 0 1
    
    open[++op]=start;
    while(op!=-1)
    {
        temp=open[op--];
        if(temp==goal){
             
             //to generate path
              j = goal;
              while(j!=start){
              		pa++;
                    path[pa]=j;
                    j=parent[j];
              }

            path[++pa]=start;
            
            //print path 
            for(i=pa;i>=0;i--)
                {   j=path[i];
                    printf("West Bank: C= %d M= %d ------- River------- East Bank: C= %d M= %d \n",state[j].cw, state[j].mw, 3-state[j].cw, 3-state[j].mw);
                  if(state[j].dir==0)
                    printf("Boat: West ===> East\n");
                  else if(state[j].dir==1&&i!=0)
                    printf("Boat: East ---> West\n");
               
                }

            return 1;}
        else
        {
          for(i=0;i<=top;i++)
                if(move(temp,i)==1&&!inList(open,i,op)&&!inList(closed,i,cl)) //if move possible from temp state ->i state 
                {open[++op]=i; parent[i]=temp;}
          closed[++cl]=temp;

        }
    }

   return 0;

}

//check if current state is valid or not 
int valid(int cw, int mw)
{int x=0,y=0;

	//if(cw+mw+=6)x=1;
	if(mw){ 
		if(mw>=cw)x=1;
	}
	else x=1;

	if(3-mw>0){ 
		if(3-mw>=3-cw)y=1;
	}
	else y=1;
       		if(x+y==2)return 1;
       		else return 0;
}


int main()
{
	//generate all valid states 
    int cw,mw,ce,me,dir;
   
                	for(cw=3;cw>=0;cw--)
                		for(mw=3;mw>=0;mw--)
                			for(dir=0;dir<=1;dir++)
    {
       if(valid(cw,mw))
       {
            push(cw,mw,dir);
            //printf("%d %d %d %d\n",cw,mw,ce,me);
        }
    }
    

    int i,j;
   
    //print all possible states
   /*
    for(i=0;i<=top;i++)
    {
        printf("%d %d %d %d dir posn %d", state[i].cw,state[i].mw, 3-state[i].cw , 3-state[i].mw, state[i].dir);
        printf("\n");
    }
    printf("%d\n", top);
	*/

   return  DFS();
}
