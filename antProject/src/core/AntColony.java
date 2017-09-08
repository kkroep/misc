//import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
//import java.awt.FontMetrics;
//import java.awt.GradientPaint;
import java.awt.Graphics2D;
//import java.awt.geom.Ellipse2D;
import java.awt.image.BufferedImage;
import java.awt.geom.Rectangle2D;
import javax.imageio.stream.*;
import java.io.File;
import java.util.*;
import java.io.IOException;

import java.lang.reflect.Constructor;
//import javax.imageio.ImageIO;

public class AntColony{
  static public void main(String args[]) throws Exception {
     try {
      int width = 128, height = 128, multiplier = 8;
      int[][][] picture = new int[width][height][3];
    
        
      String gifFileName = "../";
      String[] playerNames = new String[4];

      for(int i=0; i<4; i++){
        if(args.length>i){
            System.out.printf("%s(%d)  ", args[i], i); 
            gifFileName += args[i] + "&";
            playerNames[i] = args[i];
        }
          else{
            System.out.printf("Default(%d)  ", i); 
            gifFileName += "Default" + "&";
            playerNames[i] = "Default";
        }
      }
      System.out.printf("\n"); 

      gifFileName.substring(0,gifFileName.length() - 1);
      gifFileName += ".gif";

      // TYPE_INT_ARGB specifies the image format: 8-bit RGBA packed
      // into integer pixels
      BufferedImage bi = new BufferedImage(width*multiplier, height*multiplier, BufferedImage.TYPE_INT_ARGB);
      ImageOutputStream output = new FileImageOutputStream(new File(gifFileName));
      Graphics2D ig2 = bi.createGraphics();
      GifSequenceWriter writer = new GifSequenceWriter(output, bi.getType(), 1, false);
      //writer.writeToSequence(bi);

      ig2.setFont(new Font("TimesRoman", Font.PLAIN, 20)); 

      // initializing main Loop
      Referee referee = new Referee(50, width, height, 4);

      System.out.printf("\n%d\n", 15<<4);

      // color ideas
      int[] blue        = new int[]{20, 20, 255};
      int[] turquoise   = new int[]{064, 244, 208};
      int[] blueViolet  = new int[]{138, 043, 226};
      int[] limeGreen   = new int[]{000, 255, 000};
      int[] darkOrange  = new int[]{255, 140, 000};
      int[] fireBrick   = new int[]{170, 034, 034};

      int x = 40, y = 48; // coordinates of players, point symmetry
      int startFood = 100;

      ArrayList<Player> players = new ArrayList<Player>(){};
      players.add(new Player(blueViolet, 0, x, y, startFood, referee, playerNames[0]));
      players.add(new Player(limeGreen, 1, width-1-y, x, startFood, referee, playerNames[1]));
      players.add(new Player(darkOrange, 2, y, height-1-x, startFood, referee, playerNames[2]));
      players.add(new Player(fireBrick, 3, width-1-x, height-1-y, startFood, referee, playerNames[3]));
      //player1.draw(picture);

      // main loop
      for(int frame = 0; frame<14000; frame++){
        // clear image
        ig2.setPaint(new Color(15,15,15));
        ig2.fill(new Rectangle2D.Double(0, 0, width*multiplier, height*multiplier));
        
        // execute player turns

        for(int i=0; i<players.size(); i++){
          players.get(i).turn();
        }

        for(int i=0; i<players.size(); i++){
          players.get(i).takeDamage();
        }

        referee.turn();


        if(frame%100==0){
          if(frame%500==0){
            System.out.printf("\nF:%d\t", frame);
            for(int i=0; i<4; i++){
              if(players.get(i).colonySize()<100)
                System.out.printf(" ");
              if(players.get(i).colonySize()<10)
                System.out.printf(" ");
              System.out.printf("%d-",players.get(i).colonySize());
              System.out.printf("%d ", players.get(i).colonyFood());
              if(players.get(i).colonyFood()<1000)
                System.out.printf(" ");
              if(players.get(i).colonyFood()<100)
                System.out.printf(" ");
              if(players.get(i).colonyFood()<10)
                System.out.printf(" ");
            }
          }
          System.out.printf("-");
        }

        // only draw a few frames
        if(frame%25==0){
        //draw everything
        for(int i=0; i<width; i++)
          for(int j=0; j<height; j++)
            for(int k=0; k<3; k++)
              picture[i][j][k] = 15;

        referee.draw(picture);
        
        for(int i=0; i<players.size(); i++){
          players.get(i).draw(picture);
        }

        for(int i=0; i<width; i++)
          for(int j=0; j<height; j++)
            for(int k=0; k<3; k++)
              if(picture[i][j][k]>255)
                picture[i][j][k] = 255;

        for(int i=0; i<width; i++)
          for(int j=0; j<height; j++)
            {
              if(picture[i][j][0]!=15 || picture[i][j][1]!=15 || picture[i][j][2]!=15){
                ig2.setPaint(new Color(picture[i][j][0],picture[i][j][1],picture[i][j][2]));
                ig2.fill(new Rectangle2D.Double(i*multiplier, j*multiplier, multiplier, multiplier));
              }
            }
        ig2.setPaint(Color.white);
        ig2.drawString(String.format("Fr: %d", frame),10,20);

        for(int i=0; i<players.size(); i++){
          ig2.setPaint(new Color(players.get(i).getColor()[0],players.get(i).getColor()[1],players.get(i).getColor()[2]));
          ig2.drawString(String.format("%s(%d):  %d-%d", players.get(i).getName(), i, players.get(i).colonySize(), players.get(i).colonyFood()),10,40+20*i);
        }

        //store the image into the gif
        writer.writeToSequence(bi);
        }
      }

      System.out.printf("\n\nGame Over!\n");
      for(int i=0; i<players.size(); i++){
          System.out.printf("%s (%d): %d ants\n", players.get(i).getName(), i, players.get(i).colonySize());
      }

      // close the gif output
      writer.close();
      output.close();
    } catch (IOException ie) {
      ie.printStackTrace();
    }
}
}
