

x=zeros(102);
y=zeros(102);
xnew = zeros(102);
ynew = zeros(102);

nvplot=2;
nhplot=4;
figure

iplot = 1;
for hindex=1:2
    for vindex=1:4
    
        
        for i=1:102
            ynew(i)=sin(( (2*3.1415*i)/100.0 ));
            xnew(i)=cos(( (2*3.1415*i)/100.0 ));
        end
        
        if vindex == 1
            eps = 0.3;
        elseif vindex == 3
            eps = -0.3;
        else
            eps = 0.0;
        end
        
        for i=1:102
            y(i) = sin(( (2*3.1415*i)/100.0 ))* ( 1+eps);
            x(i) = cos(( (2*3.1415*i)/100.0 ))* ( 1-eps);
        end
        
        if vindex == 1 | vindex ==3
            if hindex == 2
              for i=1:102
               xh = x(i) * cos(-3.1415/4.0) - y(i) * sin(-3.1415/4.0);
              yh = x(i) * sin(-3.1415/4.0) - y(i) * sin(-3.1415/4.0);
              x(i) = xh;
              y(i) = yh;
             end
            end
        end
        
        subplot(nvplot,nhplot,iplot);
       
        plot(xnew,ynew,'k-')
        hold on
        axis manual
        plot(x,y,'r--','LineWidth',2)
        axis([-1.5 1.5 -1.5 1.5])
        axis off
        if vindex == 1 & hindex == 1
            title('0 degrees, + polarity')
        elseif vindex ==1 & hindex ==2
            title('0 degrees, X polarity')
        elseif vindex == 2 & hindex == 1
            title('90 degrees, + polarity')
        elseif vindex == 2 & hindex == 2
            title('90 degrees, X polarity')
        elseif vindex == 3 & hindex == 1
            title('180 degrees, + polarity') 
        elseif vindex == 3 & hindex == 2
            title('180 degrees, X polarity')
        elseif vindex == 4 & hindex == 1
            title('270 degrees, + polarity') 
        elseif vindex == 4 & hindex == 2
            title('270 degrees, X polarity')
        end
        %set(gca,'DataAspectRatio', [1 1 1]);
        iplot = iplot + 1;
    end
end
        