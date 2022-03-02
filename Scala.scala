import scala.io.Source

object ReadingFiles {
    val filepath = "/data/testscala.txt"

    val scalaFileContents: Iterator[String] = Source.fromFile(file).getLines
    scalaFileContents.foreach(println)

    def main(args: Array[String]): Unit  = {
        
    }
}